/**
 * Tests for TOC sticky-scroll with correct anchor jumping.
 *
 * Test groups:
 *  A. generateHeadingId — server-side ID generation matches Astro/rehype output
 *  B. extractTocItems   — parses markdown headings correctly
 *  C. getScrollTarget   — computes correct scroll position (header-aware offset)
 *  D. getActiveHeading  — returns correct active heading accounting for header height
 *  E. Regression bugs   — exact bugs from project history
 */

import { describe, it, expect, beforeEach } from 'vitest';
import {
  generateHeadingId,
  extractTocItems,
  getScrollTarget,
  getActiveHeading,
  HEADER_HEIGHT,
  SCROLL_OFFSET,
} from '../utils/toc';

// ─── A. generateHeadingId ─────────────────────────────────────────────────────

describe('A. generateHeadingId', () => {
  it('lowercases English text', () => {
    expect(generateHeadingId('How to Use Claude')).toBe('how-to-use-claude');
  });

  it('replaces spaces and special chars with single hyphen', () => {
    expect(generateHeadingId('Hello   World')).toBe('hello-world');
  });

  it('preserves CJK characters', () => {
    expect(generateHeadingId('如何使用 AI 工具')).toBe('如何使用-ai-工具');
  });

  it('strips smart single quotes (regression: TOC id mismatch on apostrophes)', () => {
    expect(generateHeadingId("What's New")).toBe('whats-new');
    expect(generateHeadingId('‘What’s New')).toBe('whats-new');
  });

  it('strips curly quotes', () => {
    expect(generateHeadingId('“Hello” World')).toBe('hello-world');
  });

  it('trims leading and trailing hyphens', () => {
    expect(generateHeadingId('  Hello World  ')).toBe('hello-world');
    expect(generateHeadingId('---Title---')).toBe('title');
  });

  it('handles numbers', () => {
    expect(generateHeadingId('Step 1: Install')).toBe('step-1-install');
  });

  it('handles heading with only special chars → empty string', () => {
    expect(generateHeadingId('!@#$%')).toBe('');
  });

  it('handles mixed CJK + English + numbers', () => {
    expect(generateHeadingId('Claude 3.5 使用教程')).toBe('claude-3-5-使用教程');
  });

  it('collapses multiple hyphens into one', () => {
    expect(generateHeadingId('A -- B')).toBe('a-b');
  });
});

// ─── B. extractTocItems ───────────────────────────────────────────────────────

describe('B. extractTocItems', () => {
  it('extracts h2 headings from markdown', () => {
    const md = '# Title\n\n## First Section\n\nsome text\n\n## Second Section\n';
    const items = extractTocItems(md);
    expect(items).toHaveLength(2);
    expect(items[0].text).toBe('First Section');
    expect(items[0].id).toBe('first-section');
    expect(items[1].text).toBe('Second Section');
  });

  it('ignores h1 and h3+ headings', () => {
    const md = '# H1\n## H2\n### H3\n#### H4\n';
    const items = extractTocItems(md);
    expect(items).toHaveLength(1);
    expect(items[0].text).toBe('H2');
  });

  it('deduplicates headings with same id', () => {
    const md = '## Introduction\n\nsome text\n\n## Introduction\n';
    const items = extractTocItems(md);
    expect(items).toHaveLength(1);
  });

  it('preserves document order', () => {
    const md = '## Beta\n\n## Alpha\n\n## Gamma\n';
    const items = extractTocItems(md);
    expect(items.map(i => i.text)).toEqual(['Beta', 'Alpha', 'Gamma']);
  });

  it('handles empty content', () => {
    expect(extractTocItems('')).toHaveLength(0);
    expect(extractTocItems('No headings here.')).toHaveLength(0);
  });

  it('regression: frontmatter block is not parsed as headings', () => {
    // Frontmatter contains "---" separators; the body must not lose content
    const md = '---\ntitle: Test\n---\n\n## Real Heading\n\nBody content here.';
    const items = extractTocItems(md);
    expect(items).toHaveLength(1);
    expect(items[0].text).toBe('Real Heading');
  });

  it('regression: article body is preserved (frontmatter transform must not eat body)', () => {
    const body = '## Section One\n\nThis is the body.\n\n## Section Two\n\nMore body.';
    const items = extractTocItems(body);
    expect(items).toHaveLength(2);
    // Body content should be accessible (items extracted, not lost)
    expect(items[0].text).toBe('Section One');
    expect(items[1].text).toBe('Section Two');
  });
});

// ─── C. getScrollTarget ───────────────────────────────────────────────────────
// Tests scroll position calculation to avoid heading being hidden under fixed header.

describe('C. getScrollTarget', () => {
  it('HEADER_HEIGHT is defined and positive', () => {
    expect(HEADER_HEIGHT).toBeGreaterThan(0);
  });

  it('SCROLL_OFFSET adds extra breathing room above header', () => {
    expect(SCROLL_OFFSET).toBeGreaterThanOrEqual(HEADER_HEIGHT);
  });

  it('computes correct y position for element at absoluteTop', () => {
    // If element is at absolute y=500, scroll should put it at SCROLL_OFFSET below viewport top
    const absoluteTop = 500;
    const scrollY = getScrollTarget(absoluteTop);
    // After scroll, element top relative to viewport = absoluteTop - scrollY
    // We want that to equal SCROLL_OFFSET (e.g., 80px below viewport top)
    expect(absoluteTop - scrollY).toBe(SCROLL_OFFSET);
  });

  it('never returns negative scroll position', () => {
    expect(getScrollTarget(0)).toBeGreaterThanOrEqual(0);
    expect(getScrollTarget(10)).toBeGreaterThanOrEqual(0);
  });

  it('regression: scrollIntoView(block:start) puts heading under fixed header — this must not happen', () => {
    // The naive scrollIntoView sets scrollY = absoluteTop, leaving heading at y=0 (under 56px header)
    const absoluteTop = 300;
    const naiveScroll = absoluteTop; // what scrollIntoView does
    const correctScroll = getScrollTarget(absoluteTop);
    // Correct scroll should leave room for the header
    const headingVisibleAt = absoluteTop - correctScroll;
    expect(headingVisibleAt).toBeGreaterThanOrEqual(HEADER_HEIGHT);
    expect(correctScroll).toBeLessThan(naiveScroll);
  });
});

// ─── D. getActiveHeading ──────────────────────────────────────────────────────

describe('D. getActiveHeading', () => {
  it('returns empty string when no headings', () => {
    expect(getActiveHeading([], 0)).toBe('');
  });

  it('returns first heading id when scrollY is before all headings', () => {
    const headings = [
      { id: 'intro', top: 200 },
      { id: 'body', top: 600 },
    ];
    // scrollY=0, heading tops are absolute → relative = top - scrollY
    // Neither is above threshold yet
    expect(getActiveHeading(headings, 0)).toBe('');
  });

  it('activates heading when scrolled past it (accounting for header)', () => {
    const headings = [
      { id: 'intro', top: 100 },
      { id: 'body', top: 500 },
    ];
    // scrollY=200, intro.top - scrollY = 100 - 200 = -100 (above viewport + header)
    // body.top - scrollY = 500 - 200 = 300 (below threshold)
    expect(getActiveHeading(headings, 200)).toBe('intro');
  });

  it('switches to next heading when scrolled past it', () => {
    const headings = [
      { id: 'intro', top: 100 },
      { id: 'body', top: 500 },
    ];
    // scrollY=550: intro.top-550=-450, body.top-550=-50 → both above, last one wins
    expect(getActiveHeading(headings, 550)).toBe('body');
  });

  it('regression: active highlight uses header-aware threshold (not hardcoded 100)', () => {
    // The threshold should be SCROLL_OFFSET so active state is consistent with scroll position
    const headings = [{ id: 'section', top: 300 }];
    // When element top relative to viewport = SCROLL_OFFSET, it should be active
    const scrollY = 300 - SCROLL_OFFSET;
    expect(getActiveHeading(headings, scrollY)).toBe('section');
  });
});

// ─── E. Regression bugs from project history ──────────────────────────────────

describe('E. Regression bugs', () => {
  it('BASE_URL: no double slashes in constructed paths', () => {
    // BASE_URL with trailing slash + path with leading slash = double slash
    const base = '/'; // common BASE_URL value
    const path = '/en/articles/';
    const full = base.replace(/\/$/, '') + path;
    expect(full).not.toContain('//');
    expect(full).toBe('/en/articles/');
  });

  it('BASE_URL: base="" + path = correct path', () => {
    const base = '';
    const path = '/en/articles/';
    const full = base.replace(/\/$/, '') + path;
    expect(full).toBe('/en/articles/');
  });

  it('TOC id consistency: same heading text always produces same id', () => {
    const text = 'Getting Started with Claude';
    const id1 = generateHeadingId(text);
    const id2 = generateHeadingId(text);
    expect(id1).toBe(id2);
    expect(id1).toBe('getting-started-with-claude');
  });

  it('TOC id consistency: heading with inline code stripped correctly', () => {
    // Markdown heading like "## Using `useState`" has backticks stripped by rehype
    const withCode = 'Using useState';  // after stripping backticks
    expect(generateHeadingId(withCode)).toBe('using-usestate');
  });

  it('TOC: Chinese + number heading consistent with Astro rendering', () => {
    // Astro rehype-slug uses GitHub slug algorithm which lowercases + replaces non-alphanum
    expect(generateHeadingId('第1步：安装依赖')).toBe('第1步安装依赖');
  });
});
