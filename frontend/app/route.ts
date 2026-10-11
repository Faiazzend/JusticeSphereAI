import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const htmlPath = path.join(process.cwd(), 'public', 'index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    return new NextResponse(html, {
      status: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
      },
    });
  } catch (error) {
    return new NextResponse(
      '<h1>ContractMind v1.5</h1><p>Unable to load studio UI.</p>',
      {
        status: 500,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      }
    );
  }
}
