import { z, defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        pageLabel: z.string().optional(),
        sourceCount: z.number().int().positive().optional(),
        publishedAt: z.string().optional(),
        sourceUrl: z.string().url().optional()
      })
    })
  })
};
