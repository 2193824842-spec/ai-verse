/**
 * TOC utilities — pure functions extracted from [slug].astro
 * for testability and consistency between server-side and client-side ID generation.
 */

/** Fixed header height in px (matches CSS --header-h: 56px + 24px breathing room) */
export const HEADER_HEIGHT = 56;

/** Scroll offset: heading appears this many px below the viewport top after jump */
export const SCROLL_OFFSET = 80;

/**
 * Generate a heading anchor ID that matches Astro/rehype-slug output.
 * Must be called with the same text on both server (TOC extraction) and
 * client (DOM id assignment) to guarantee consistency.
 */
export function generateHeadingId(text: string): string {
  return text
    .toLowerCase()
    // Strip smart/curly quotes and straight apostrophes (using unicode escapes to avoid parse errors)
    .replace(/[‘’ʼ“”']/g, '')
    // Strip full-width and CJK punctuation (U+3000-U+303F, U+FF00-U+FFEF)
    // These are removed, not turned into hyphens, to match rehype-slug output
    .replace(/[　-〿＀-￯]/g, '')
    // Replace any run of non-word, non-CJK characters with a single hyphen
    .replace(/[^\w一-鿿]+/g, '-')
    // Trim leading/trailing hyphens
    .replace(/^-+|-+$/g, '');
}

export interface TocItem {
  level: number;
  text: string;
  id: string;
}

/**
 * Extract h2 TOC items from raw markdown body.
 * Skips frontmatter block. Deduplicates by id. Preserves document order.
 */
export function extractTocItems(rawContent: string): TocItem[] {
  // Strip frontmatter block (--- ... ---) before parsing
  const body = rawContent.replace(/^---[\s\S]*?---\s*/m, '');

  const items: TocItem[] = [];
  const seenIds = new Set<string>();

  const mdHeadingRegex = /^(#{2,3})\s+(.+)$/gm;
  let match: RegExpExecArray | null;

  while ((match = mdHeadingRegex.exec(body)) !== null) {
    if (match[1].length !== 2) continue; // only h2
    const text = match[2].trim();
    const id = generateHeadingId(text);
    if (seenIds.has(id)) continue;
    seenIds.add(id);
    items.push({ level: 2, text, id });
  }

  return items;
}

/**
 * Given the absolute top position of a heading element (offsetTop from document top),
 * return the window.scrollY value that places the heading SCROLL_OFFSET px below
 * the viewport top - i.e., just below the fixed header with breathing room.
 */
export function getScrollTarget(absoluteTop: number): number {
  return Math.max(0, absoluteTop - SCROLL_OFFSET);
}

export interface HeadingPosition {
  id: string;
  /** Absolute top of the heading (element.offsetTop) */
  top: number;
}

/**
 * Given a list of heading positions and the current scrollY,
 * return the id of the heading that should be highlighted as active.
 *
 * A heading is "active" when the user has scrolled past it
 * (its top is within SCROLL_OFFSET px of the viewport top or above it).
 * Returns the last heading that satisfies this condition.
 */
export function getActiveHeading(
  headings: HeadingPosition[],
  scrollY: number,
): string {
  let current = '';
  for (const h of headings) {
    // Relative position to viewport top
    const relativeTop = h.top - scrollY;
    if (relativeTop <= SCROLL_OFFSET) {
      current = h.id;
    }
  }
  return current;
}
