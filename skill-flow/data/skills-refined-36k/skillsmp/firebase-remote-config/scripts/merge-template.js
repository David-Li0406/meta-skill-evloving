#!/usr/bin/env node
import fs from 'fs';

const args = process.argv.slice(2);
const base = args.find(a=>a.startsWith('--base')).split('=')[1];
const upd  = args.find(a=>a.startsWith('--updates')).split('=')[1];
const out  = args.find(a=>a.startsWith('--out')).split('=')[1];

const baseJson = JSON.parse(fs.readFileSync(base));
const updJson  = JSON.parse(fs.readFileSync(upd));

baseJson.parameters = {...baseJson.parameters, ...updJson.parameters};
baseJson.conditions = [...baseJson.conditions, ...updJson.conditions];

fs.writeFileSync(out, JSON.stringify(baseJson, null, 2));
