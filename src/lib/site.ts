/**
 * Single source of truth for site-wide metadata and verified facts.
 * Every number here is traceable in docs/content-provenance.md.
 */

export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const p = path.startsWith('/') ? path : `/${path}`;
  return `${base}${p}`;
}

export const SITE = {
  title: 'Probing the World for Groove',
  shortTitle: 'Probing the World for Groove',
  hero: 'Can a model trained on general audio understand drum style?',
  tagline:
    'A comparison of a drum-specific CNN and frozen PaSST transfer learning across 18,264 two-bar grooves and 74 style labels.',
  description:
    'A controlled comparison of a task-specific CNN and a pretrained PaSST audio transformer for drum-pattern style classification from two-bar audio, for the MSc thesis and ISMIR 2025 Late-Breaking Demo by Trent Eriksen.',
  author: 'Trent Eriksen',
  authors: ['Trent Eriksen', 'Edwin van der Heide', 'Robert Saunders'],
  siteUrl: 'https://grashopr-888.github.io',
  basePath: '/probing-the-world-for-groove',
} as const;

export const NAV = [
  { label: 'Overview', href: '/' },
  { label: 'Method', href: '/method' },
  { label: 'Experiments', href: '/experiments' },
  { label: 'Representations', href: '/representations' },
  { label: 'ISMIR 2025', href: '/publication' },
  { label: 'Resources', href: '/resources' },
] as const;

/** Headline figures. See content-provenance.md #1-#5 */
export const KEY_FACTS = [
  { value: '18,264', label: 'two-bar clips', note: 'Groove MIDI Dataset, rendered to audio' },
  { value: '74', label: 'style classes', note: 'primary ⊕ secondary annotations' },
  { value: '34', label: 'experiments', note: 'across 11 rounds' },
  { value: '11', label: 'rounds', note: 'in 4 thematic categories' },
] as const;

/** The two comparable headline results. Provenance #6 & #8 */
export const HEADLINE = {
  cnn: { f1: 0.908, exp: '10.1', config: '7-conv CNN · Gaussian noise + room simulation' },
  passt: { f1: 0.8752, exp: '11.2', config: 'frozen PaSST · 4-layer MLP · reflection padding' },
} as const;

/** The low-data reversal. Provenance #10 & #11 */
export const LOWDATA = {
  cnn: 0.3267,
  passt: 0.3911,
  scope: 'GMD-mini (≈10% subset)',
} as const;

export const LINKS = {
  // Curated notebook archive with reconstructed commit history (canonical for notebook links)
  archiveRepo: 'https://github.com/Grashopr-888/drum-style-thesis-notebooks',
  repo: 'https://github.com/Grashopr-888/A-comparative-study-of-Transfer-Learning-for-Drum-audio-Style-Classification-',
  ismir: 'https://ismir2025program.ismir.net/lbd_456.html',
  video: 'https://youtu.be/f_nIl5qMxlY',
  videoId: 'f_nIl5qMxlY',
  // external references
  gmd: 'https://www.tensorflow.org/datasets/catalog/groove',
  passt: 'https://github.com/kkoutini/passt_hear21',
  drumClassification: 'https://github.com/khiner/DrumClassification',
  audiomentations: 'https://github.com/iver56/audiomentations',
  audioExamples: 'https://drive.google.com/drive/folders/1taQUOIU8z7aKlKEZvoMsV9u3fP7IBS_C',
} as const;

/** Local downloadable assets (live in /public, served under base) */
export const ASSETS = {
  thesisPdf: '/papers/probing-the-world-for-groove-thesis.pdf',
  lbdPdf: '/papers/ismir2025-lbd-eriksen.pdf',
  posterPdf: '/poster/ismir2025-poster-eriksen.pdf',
  workbook: '/data/thesis-experiment-results.xlsx',
} as const;

export const PUBLICATION = {
  thesisTitle:
    'Probing the World for Groove: A Comparative Study of Transfer Learning for Drum Audio Style Classification',
  lbdTitle: 'A Comparative Study of Transfer Learning for Drum Audio Style Classification',
  degree: 'MSc Media Technology, Leiden Institute of Advanced Computer Science (LIACS), Leiden University',
  thesisDate: '30 June 2025',
  supervisors: ['Edwin van der Heide', 'Dr. Robert Saunders'],
  venue: 'Late-Breaking / Demo Session, 26th International Society for Music Information Retrieval Conference (ISMIR 2025)',
  venueLocation: 'Daejeon, South Korea',
  license: 'CC BY 4.0',
} as const;
