#!/usr/bin/env python3
from __future__ import annotations

import html
import hashlib
import os
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VAULT = ROOT.parent.parent / "Desktop" / "obsidian"
SITE_BASE = "/auto-drive"
WIKI_DIRNAME = "wiki"
RAW_DIRNAME = "raw"
DOCS_DIR = ROOT / "src" / "content" / "docs"
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
LEADING_H1_RE = re.compile(r"^\s*#\s+.+?(?:\n+|$)", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RAW_LEADING_NOISE_RE = re.compile(r'^\[\d+\]\(#\s*"点击查看跟贴"\)$')

WIKI_PAGE_LABELS = {
    "overview": "总览",
    "themes": "主题",
    "companies": "公司档案",
    "people": "人物档案",
    "sources": "来源索引",
}


@dataclass
class Page:
    source_path: Path
    rel_source: Path
    output_rel: Path
    title: str
    frontmatter: dict[str, object]
    body: str
    section: str
    excerpt: str
    page_label: str


def vault_root() -> Path:
    configured = os.environ.get("AUTO_DRIVE_VAULT")
    path = Path(configured).expanduser() if configured else DEFAULT_VAULT
    return path.resolve()


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw_frontmatter = text[4:end]
            body = text[end + 5 :]
            frontmatter = yaml.safe_load(raw_frontmatter) or {}
            if not isinstance(frontmatter, dict):
                frontmatter = {}
            return frontmatter, body.lstrip("\n")
    return {}, text


def extract_title(frontmatter: dict[str, object], body: str, fallback: str) -> str:
    title = frontmatter.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def short_slug(value: str) -> str:
    slug = value.lower().strip()
    slug = slug.replace("·", "-")
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    if slug:
        return slug[:48]
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"note-{digest}"


def page_output_path(rel_source: Path) -> Path:
    if rel_source == Path("wiki/index.md"):
        return Path("site-index.md")
    if rel_source == Path("wiki/log.md"):
        return Path("log.md")
    if rel_source.parts[0] == WIKI_DIRNAME:
        relative = rel_source.relative_to(WIKI_DIRNAME)
        folder = Path(*relative.parts[:-1]) if len(relative.parts) > 1 else Path()
        return folder / f"{short_slug(relative.stem)}.md"
    return Path("raw") / f"{short_slug(rel_source.stem)}.md"


def trim_raw_boilerplate(body: str) -> str:
    lines = body.lstrip().splitlines()

    while lines:
        candidate = lines[0].strip()
        if not candidate:
            lines.pop(0)
            continue
        if candidate == "分享至" or RAW_LEADING_NOISE_RE.match(candidate):
            lines.pop(0)
            continue
        break

    while lines:
        candidate = lines[-1].strip()
        if not candidate:
            lines.pop()
            continue
        if candidate.startswith("特别声明：以上内容") or candidate.startswith("Notice: The content above"):
            lines.pop()
            continue
        break

    return "\n".join(lines).strip()


def normalize_body(body: str, section: str) -> str:
    normalized = body
    if section == RAW_DIRNAME:
        normalized = trim_raw_boilerplate(normalized)
    return normalized.strip()


def plain_text_excerpt(block: str) -> str:
    block = re.sub(r"\((?:[^()]*(?:raw/|https?://)[^()]*)\)", "", block)
    if "(" in block:
        block = block.split("(", 1)[0].rstrip(" ，,;；")
    cleaned = re.sub(r"[*`>\-\[\]()]"," ", block)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def excerpt_from_body(body: str, section: str) -> str:
    text = normalize_body(body, section)
    text = WIKILINK_RE.sub(lambda match: parse_wikilink(match.group(1))[1], text)
    text = MARKDOWN_LINK_RE.sub(lambda match: match.group(1), text)
    text = LEADING_H1_RE.sub("", text, count=1).strip()
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    for block in blocks:
        if block.startswith(("#", "-", "*", ">", "|", "```")):
            continue
        cleaned = plain_text_excerpt(block)
        if not cleaned or cleaned.isdigit() or cleaned in {"分享至"} or len(cleaned) < 8:
            continue
        if cleaned:
            return cleaned[:180]
    cleaned = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    cleaned = re.sub(r"[*`>\-\[\]()]"," ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:180]


def page_label_for_source(rel_source: Path) -> str:
    if rel_source.parts[0] == RAW_DIRNAME:
        return "原始材料"
    if rel_source == Path("wiki/log.md"):
        return "更新日志"
    if rel_source == Path("wiki/index.md"):
        return "全站索引"
    if len(rel_source.parts) > 1:
        return WIKI_PAGE_LABELS.get(rel_source.parts[1], "判断档案")
    return "判断档案"


def page_group(page: Page) -> str:
    if page.section == RAW_DIRNAME:
        return RAW_DIRNAME
    if page.rel_source == Path("wiki/index.md"):
        return "site-index"
    if page.rel_source == Path("wiki/log.md"):
        return "log"
    if len(page.rel_source.parts) > 1:
        return page.rel_source.parts[1]
    return "other"


def build_page_catalog(vault: Path) -> tuple[list[Page], dict[str, Page]]:
    pages: list[Page] = []
    page_map: dict[str, Page] = {}
    source_paths = sorted((vault / WIKI_DIRNAME).rglob("*.md")) + sorted((vault / RAW_DIRNAME).rglob("*.md"))

    for source_path in source_paths:
        rel_source = source_path.relative_to(vault)
        frontmatter, body = parse_markdown(source_path)
        title = extract_title(frontmatter, body, source_path.stem)
        page = Page(
            source_path=source_path,
            rel_source=rel_source,
            output_rel=page_output_path(rel_source),
            title=title,
            frontmatter=frontmatter,
            body=body.rstrip() + "\n",
            section=rel_source.parts[0],
            excerpt=excerpt_from_body(body, rel_source.parts[0]),
            page_label=page_label_for_source(rel_source),
        )
        pages.append(page)
        if page.section == WIKI_DIRNAME:
            page_map[str(rel_source.relative_to(WIKI_DIRNAME).with_suffix(""))] = page
            if rel_source == Path("wiki/index.md"):
                page_map["index"] = page
            if rel_source == Path("wiki/log.md"):
                page_map["log"] = page
        else:
            page_map[str(rel_source.with_suffix(""))] = page

    return pages, page_map


def route_dir(output_rel: Path) -> Path:
    if output_rel == Path("index.md"):
        return Path(".")
    return output_rel.with_suffix("")


def relative_link_from_output(source_output: Path, target_output: Path) -> str:
    source_dir = route_dir(source_output)
    target_dir = route_dir(target_output)
    rel = os.path.relpath(target_dir, start=source_dir).replace(os.sep, "/")
    if rel == ".":
        return "./"
    return rel.rstrip("/") + "/"


def relative_link(source_page: Page, target_page: Page) -> str:
    return relative_link_from_output(source_page.output_rel, target_page.output_rel)


def absolute_link_from_output(target_output: Path) -> str:
    target_dir = route_dir(target_output)
    if target_dir == Path("."):
        return f"{SITE_BASE}/"
    target_path = target_dir.as_posix().strip("/")
    return f"{SITE_BASE}/{target_path}/"


def parse_wikilink(raw: str) -> tuple[str, str]:
    value = raw.strip()
    if "|" in value:
        target, label = value.split("|", 1)
        return target.strip(), label.strip()
    return value, Path(value).name


def convert_wikilinks(body: str, page: Page, page_map: dict[str, Page]) -> str:
    def replace(match: re.Match[str]) -> str:
        target, label = parse_wikilink(match.group(1))
        target_page = page_map.get(target)
        if target_page is None:
            return label
        return f"[{label}]({absolute_link_from_output(target_page.output_rel)})"

    return WIKILINK_RE.sub(replace, body)


def linked_pages(page: Page, page_map: dict[str, Page]) -> list[Page]:
    found: list[Page] = []
    seen: set[Path] = set()
    for match in WIKILINK_RE.finditer(page.body):
        target, _label = parse_wikilink(match.group(1))
        target_page = page_map.get(target)
        if target_page is None or target_page.output_rel == page.output_rel or target_page.output_rel in seen:
            continue
        seen.add(target_page.output_rel)
        found.append(target_page)
    return found


def parse_iso_date(value: object) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        try:
            return date.fromisoformat(stripped)
        except ValueError:
            return None
    return None


def strip_leading_title(body: str, title: str) -> str:
    lines = body.lstrip().splitlines()
    if lines and lines[0].strip() == f"# {title}":
        return "\n".join(lines[1:]).lstrip("\n")
    return LEADING_H1_RE.sub("", body, count=1).lstrip("\n")


def trim_duplicate_lead(body: str, excerpt: str) -> str:
    blocks = [block for block in re.split(r"\n\s*\n", body.strip()) if block.strip()]
    if len(blocks) < 2 or not excerpt:
        return body
    first_clean = plain_text_excerpt(MARKDOWN_LINK_RE.sub(lambda match: match.group(1), blocks[0]))
    excerpt_clean = plain_text_excerpt(excerpt)
    if not first_clean or not excerpt_clean:
        return body
    if first_clean == excerpt_clean or first_clean.startswith(excerpt_clean) or excerpt_clean.startswith(first_clean):
        return "\n\n".join(blocks[1:]).strip()
    return body


def build_frontmatter(page: Page) -> dict[str, object]:
    data: dict[str, object] = {
        "title": "全站索引" if page.rel_source == Path("wiki/index.md") else page.title,
        "description": page.excerpt or page.title,
        "pageLabel": page.page_label,
    }

    updated = parse_iso_date(page.frontmatter.get("updated"))
    if updated:
        data["lastUpdated"] = updated

    source_count = page.frontmatter.get("source_count")
    if isinstance(source_count, int):
        data["sourceCount"] = source_count

    published = parse_iso_date(page.frontmatter.get("published"))
    if published:
        data["publishedAt"] = published.isoformat()

    source_url = page.frontmatter.get("source")
    if isinstance(source_url, str) and source_url.startswith(("http://", "https://")):
        data["sourceUrl"] = source_url

    return data


def render_recommendation_section(page: Page, pages: list[Page], page_map: dict[str, Page]) -> str:
    current_group = page_group(page)
    if current_group not in {"companies", "people"}:
        return ""

    target_group = "people" if current_group == "companies" else "companies"
    target_title = "相关人物" if current_group == "companies" else "相关公司"

    recommendations: list[Page] = []
    seen: set[Path] = set()

    for candidate in linked_pages(page, page_map):
        if page_group(candidate) != target_group or candidate.output_rel in seen:
            continue
        seen.add(candidate.output_rel)
        recommendations.append(candidate)
        if len(recommendations) >= 3:
            break

    if len(recommendations) < 3:
        for candidate in pages:
            if page_group(candidate) != target_group or candidate.output_rel in seen:
                continue
            candidate_links = linked_pages(candidate, page_map)
            if any(linked.output_rel == page.output_rel for linked in candidate_links):
                seen.add(candidate.output_rel)
                recommendations.append(candidate)
                if len(recommendations) >= 3:
                    break

    if not recommendations:
        return ""

    cards = []
    for recommendation in recommendations:
        cards.append(
            f"""
<a class="related-card" href="{absolute_link_from_output(recommendation.output_rel)}">
  <span class="related-card-title">{html.escape(recommendation.title)}</span>
  <span class="related-card-desc">{html.escape(recommendation.excerpt or recommendation.title)}</span>
</a>
""".strip()
        )

    return "\n".join(
        [
            "## 继续阅读",
            "",
            '<div class="related-grid">',
            *cards,
            "</div>",
        ]
    )


def compile_page(page: Page, pages: list[Page], page_map: dict[str, Page]) -> str:
    frontmatter = build_frontmatter(page)
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    body = normalize_body(page.body, page.section)
    body = convert_wikilinks(body, page, page_map)
    body = strip_leading_title(body, page.title).strip()
    body = trim_duplicate_lead(body, page.excerpt)
    related = render_recommendation_section(page, pages, page_map)
    if related:
        body = "\n\n".join([body, related]).strip()

    compiled_parts = [
        "---",
        yaml_block,
        "---",
        "",
        body,
        "",
    ]
    return "\n".join(compiled_parts)


def make_link(source_output: Path, target_page: Page, label: str) -> str:
    return f"[{label}]({absolute_link_from_output(target_page.output_rel)})"


def make_url(source_output: Path, target_page: Page) -> str:
    return absolute_link_from_output(target_page.output_rel)


def require_page(page_map: dict[str, Page], key: str) -> Page:
    page = page_map.get(key)
    if page is None:
        raise SystemExit(f"Missing required page target: {key}")
    return page


def card_link(page: Page) -> str:
    return absolute_link_from_output(page.output_rel)


def render_entry_card(page: Page) -> str:
    return f"""
<a class="index-card" href="{card_link(page)}">
  <span class="index-card-title">{html.escape(page.title)}</span>
  <span class="index-card-desc">{html.escape(page.excerpt or page.title)}</span>
</a>
""".strip()


def render_section_card(title: str, intro: str, items: list[tuple[Page, str]]) -> str:
    links = []
    for page, description in items:
        links.append(
            f"""
<a class="landing-link" href="{card_link(page)}">
  <span class="landing-link-title">{html.escape(page.title)}</span>
  <span class="landing-link-desc">{html.escape(description)}</span>
</a>
""".strip()
        )
    return f"""
<section class="landing-card">
  <div class="landing-card-header">
    <span class="landing-card-kicker">{title}</span>
    <p>{intro}</p>
  </div>
  <div class="landing-links">
    {' '.join(links)}
  </div>
</section>
""".strip()


def build_site_index(pages: list[Page], *, root: bool = False) -> str:
    frontmatter = {
        "title": "全站索引" if root else "目录浏览",
        "description": "按主题、公司、人物和资料来源浏览全部内容。每张卡片都带有摘要，方便快速判断是否值得点开。",
    }

    groups: dict[str, list[Page]] = defaultdict(list)
    for page in pages:
        group = page_group(page)
        if group in {"site-index"}:
            continue
        groups[group].append(page)

    group_meta = [
        ("overview", "行业框架"),
        ("themes", "主题"),
        ("companies", "公司"),
        ("people", "人物"),
        ("sources", "资料索引"),
        ("raw", "参考资料"),
        ("log", "最近更新"),
    ]

    sections: list[str] = []
    for group_key, label in group_meta:
        entries = sorted(groups.get(group_key, []), key=lambda page: page.title)
        if not entries:
            continue
        cards = "\n".join(render_entry_card(page) for page in entries)
        sections.append(
            "\n".join(
                [
                    f"## {label}",
                    "",
                    '<div class="index-grid">',
                    cards,
                    "</div>",
                ]
            )
        )

    body = "\n\n".join(
        [
            "这页适合带着明确问题来时快速浏览。每张卡片都附带摘要，先判断相关性，再决定是否点开细读。",
            *sections,
        ]
    )
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return "\n".join(["---", yaml_block, "---", "", body, ""])


def build_raw_landing(page_map: dict[str, Page]) -> str:
    output_rel = Path("raw/index.md")
    cfo = require_page(page_map, "raw/对话小马智行CFO王皓俊：自动驾驶行业最大的竞争对手是自己")
    robotaxi = require_page(page_map, "raw/Robotaxi 出故障，不能只会停在半路")
    momenta = require_page(page_map, "raw/对话Momenta曹旭东：智驾航海家、多发钱的CEO和“吃狗粮”的人｜远光灯")

    frontmatter = {
        "title": "参考资料",
        "description": "这里保留外部 vault 中整理过的资料原文，适合在读完正文后回到语境核对证据。",
        "pageLabel": "原始材料",
    }
    body = f"""
这里保留的是资料原文。建议先读行业框架、主题、公司或人物页，再回到这里核对出处、语境和表述细节。

## 建议这样使用

- 把这里当作证据库，而不是第一次进入本站时的主菜。
- 当你想确认一句判断是怎么来的，就从正文页底部的来源链接回到这里。
- 当你想重新理解某个玩家的口气、框架和隐含约束时，再读整篇原文。

## 从这里开始

- {make_link(output_rel, cfo, "小马智行 CFO 对话")}
- {make_link(output_rel, momenta, "Momenta 曹旭东对话")}
- {make_link(output_rel, robotaxi, "Robotaxi 故障与可靠性")}
""".strip()
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return "\n".join(["---", yaml_block, "---", "", body, ""])


def reset_docs_dir() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def write_manual_pages(page_map: dict[str, Page]) -> None:
    unique_pages = {page.output_rel: page for page in page_map.values()}
    pages = sorted(unique_pages.values(), key=lambda page: page.output_rel.as_posix())
    manual_pages = {
        DOCS_DIR / "index.md": build_site_index(pages, root=True),
        DOCS_DIR / "raw" / "index.md": build_raw_landing(page_map),
    }
    for path, content in manual_pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def write_compiled_docs(vault: Path) -> int:
    pages, page_map = build_page_catalog(vault)
    reset_docs_dir()
    write_manual_pages(page_map)

    for page in pages:
        if page.rel_source == Path("wiki/index.md"):
            continue
        output_path = DOCS_DIR / page.output_rel
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(compile_page(page, pages, page_map), encoding="utf-8")

    return len(pages)


def main() -> None:
    vault = vault_root()
    if not (vault / WIKI_DIRNAME).exists():
        raise SystemExit(f"Missing wiki directory under {vault}")
    if not (vault / RAW_DIRNAME).exists():
        raise SystemExit(f"Missing raw directory under {vault}")

    count = write_compiled_docs(vault)
    print(f"Compiled {count} pages into {DOCS_DIR}")


if __name__ == "__main__":
    main()
