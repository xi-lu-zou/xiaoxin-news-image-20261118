// news-image-20261118 entry (Node 22, standard library only).
// The entry image is entry.png beside this file — a front-page collage of the
// world news of Wednesday 18 November 2026, drawn by make_image.py (kept in
// this repository as the image's provenance). This program copies entry.png
// to the output directory as entry.png, which is the file the judge sees.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(src);
// Sanity-check the asset before handing it over: it must be a whole PNG
// (8-byte signature) of at most 1 MiB, the gate's limits for this bounty.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (bytes.length > 1_048_576) throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
if (!PNG_SIGNATURE.every((b, i) => bytes[i] === b)) throw new Error('entry.png does not start with a PNG signature');

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
console.log(`wrote ${dest} (${bytes.length} bytes, PNG, sums up Wednesday 18 November 2026)`);
