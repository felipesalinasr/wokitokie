#!/usr/bin/env node
const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const readline = require('readline');

const FLAG_FILE = '/tmp/claude-voice-active';
const PID_FILE = '/tmp/claude-thinking.pid';
const PLUGIN_ROOT = path.resolve(__dirname, '..');

const cmd = process.argv[2];

const help = `
  wokitokie — voice-to-voice mode for Claude Code

  Usage:
    npx wokitokie install     Install as Claude Code plugin
    npx wokitokie on          Enable voice mode
    npx wokitokie off         Disable voice mode
    npx wokitokie generate    Generate thinking sound clips
    npx wokitokie status      Check if voice mode is active
    npx wokitokie help        Show this help
`;

function killAudio() {
  try { execSync('pkill -9 -x afplay 2>/dev/null', { stdio: 'ignore' }); } catch {}
  if (fs.existsSync(PID_FILE)) {
    try {
      const pid = fs.readFileSync(PID_FILE, 'utf8').trim();
      if (/^\d+$/.test(pid)) process.kill(Number(pid), 9);
    } catch {}
    try { fs.unlinkSync(PID_FILE); } catch {}
  }
}

switch (cmd) {
  case 'install': {
    console.log('Installing wokitokie as a Claude Code plugin...');
    try {
      execSync('claude plugin add wokitokie', { stdio: 'inherit' });
      console.log('\nDone! Now:');
      console.log('  1. Set your ElevenLabs key: export ELEVENLABS_API_KEY="your-key"');
      console.log('  2. Generate thinking clips: npx wokitokie generate');
      console.log('  3. In Claude Code, run: /voice-on');
    } catch {
      console.error('Failed. Make sure Claude Code CLI is installed.');
      process.exit(1);
    }
    break;
  }

  case 'on': {
    fs.writeFileSync(FLAG_FILE, '');
    console.log('Voice mode ON');
    break;
  }

  case 'off': {
    try { fs.unlinkSync(FLAG_FILE); } catch {}
    killAudio();
    console.log('Voice mode OFF');
    break;
  }

  case 'generate': {
    if (!process.env.ELEVENLABS_API_KEY) {
      console.error('Error: ELEVENLABS_API_KEY not set');
      console.error('Set it with: export ELEVENLABS_API_KEY="your-key"');
      process.exit(1);
    }
    console.log('Generating thinking sound clips...');
    const script = path.join(PLUGIN_ROOT, 'hooks', 'scripts', 'generate-thinking-sounds.py');
    const child = spawn('python3', [script], {
      stdio: 'inherit',
      env: { ...process.env, CLAUDE_PLUGIN_ROOT: PLUGIN_ROOT },
    });
    child.on('exit', (code) => process.exit(code || 0));
    break;
  }

  case 'status': {
    const active = fs.existsSync(FLAG_FILE);
    console.log(`Voice mode: ${active ? 'ON' : 'OFF'}`);
    break;
  }

  case 'help':
  case '--help':
  case '-h':
  case undefined: {
    console.log(help);
    break;
  }

  default: {
    console.error(`Unknown command: ${cmd}`);
    console.log(help);
    process.exit(1);
  }
}
