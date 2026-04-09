import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://erpeng.github.io',
  base: '/auto-drive',
  integrations: [
    starlight({
      title: '自动驾驶阅读手册',
      description: '把自动驾驶行业里的公司、人物、分歧和参考资料，整理成一个持续更新的阅读站点。',
      customCss: ['./src/styles/custom.css'],
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN'
        }
      },
      defaultLocale: 'root',
      components: {
        PageTitle: './src/components/PageTitle.astro'
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/erpeng/auto-drive'
        }
      ],
      sidebar: [
        {
          label: '行业框架',
          autogenerate: { directory: 'overview' }
        },
        {
          label: '主题',
          autogenerate: { directory: 'themes' }
        },
        {
          label: '公司',
          autogenerate: { directory: 'companies' }
        },
        {
          label: '人物',
          autogenerate: { directory: 'people' }
        },
        {
          label: '资料索引',
          autogenerate: { directory: 'sources' }
        },
        {
          label: '参考资料',
          collapsed: true,
          autogenerate: { directory: 'raw', collapsed: true }
        }
      ]
    })
  ]
});
