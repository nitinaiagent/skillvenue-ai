# AI Terms You Should Know: AI Agent Café

A plain-English catalogue of **360 AI terms**. Each entry has a 2–3 sentence explanation, a real-world example, a difficulty level (Beginner / Practitioner / Advanced) and a status tag (New / Trending / Established).

The site lives at **https://skillvenue.com**. It's curated by Nitin Monga · [AI Agent Café](https://aiagentcafe.com).

Design: the AI Agent Café dark slide template. It uses a pure black background, the teal → magenta → purple → blue gradient, the teal robot logo, and Bricolage Grotesque + IBM Plex fonts. Every page has a branded header and footer, and the terms appear as numbered cards stacked vertically.

```
index.html          ← the built site (what GitHub Pages serves)
data/terms.json     ← SOURCE OF TRUTH: every term lives here
build/template.html ← page design
build/build.py      ← regenerates index.html + sitemap.xml from terms.json
assets/logo.svg     ← AI Agent Café teal logo (also the favicon); logo.png for link previews
CNAME               ← tells GitHub Pages to serve the site on skillvenue.com
.nojekyll, robots.txt, sitemap.xml
```

---

## Deploy to GitHub Pages on skillvenue.com

### Step 1: Create the repository
1. Sign in at https://github.com and go to https://github.com/new.
2. Name it `skillvenue-ai-glossary`, set it to **Public**, and leave "Add a README" **unticked**.
3. Click **Create repository**.

### Step 2: Upload the files
Choose one of these options.

**Option A: in the browser (no Git needed)**
1. On the new repo page, click **uploading an existing file**.
2. Unzip the folder on your computer. Open it, select **everything inside it** (including the hidden `.nojekyll` file; on Mac press `Cmd+Shift+.` to show hidden files) and drag it all into the page.
3. Click **Commit changes**.

**Option B: from the terminal**
```bash
cd skillvenue-ai-glossary
git init
git add .
git commit -m "Launch AI glossary"
git branch -M main
git remote add origin https://github.com/<your-username>/skillvenue-ai-glossary.git
git push -u origin main
```

### Step 3: Turn on GitHub Pages
1. In the repo, go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to *Deploy from a branch*, **Branch** to `main`, and the folder to `/ (root)`. Then click **Save**.
3. Under **Custom domain**, enter `skillvenue.com` and click **Save**.
4. Within about a minute the site is also live at `https://<your-username>.github.io/skillvenue-ai-glossary/`, which is useful for a quick check.

### Step 4: Point skillvenue.com at GitHub
Log in to the company where **skillvenue.com is registered** (GoDaddy, Namecheap, Hostinger, BigRock, etc.) and open its **DNS / Manage DNS** page.

1. **Delete** any existing `A` records for `@` and any `CNAME` for `www`, such as parking or "coming soon" records.
2. **Add** these records:

| Type  | Host / Name | Value / Points to            | TTL     |
|-------|-------------|------------------------------|---------|
| A     | @           | 185.199.108.153              | default |
| A     | @           | 185.199.109.153              | default |
| A     | @           | 185.199.110.153              | default |
| A     | @           | 185.199.111.153              | default |
| AAAA  | @           | 2606:50c0:8000::153          | default |
| AAAA  | @           | 2606:50c0:8001::153          | default |
| AAAA  | @           | 2606:50c0:8002::153          | default |
| AAAA  | @           | 2606:50c0:8003::153          | default |
| CNAME | www         | `<your-username>.github.io`  | default |

The AAAA records are optional but recommended. Some registrars label the host `@` as blank or as "skillvenue.com".

### Step 5: Wait, then switch on HTTPS
1. DNS usually updates in 10–60 minutes; it can take up to 24 hours. To check, run `dig skillvenue.com +short` (Mac/Linux) or `nslookup skillvenue.com` (Windows). You should see the four `185.199.x.153` addresses.
2. Back in **Settings → Pages**, the domain check turns green ("DNS check successful").
3. Tick **Enforce HTTPS**. If it's greyed out, GitHub is still issuing the free certificate; check back in a few minutes.
4. Open https://skillvenue.com. `www.skillvenue.com` redirects there automatically.

### Step 6 (recommended): Verify the domain on GitHub
Go to your **profile Settings → Pages → Add a domain**, enter `skillvenue.com`, and add the TXT record GitHub shows you at your registrar. This stops anyone else from pointing a GitHub site at your domain.

### Troubleshooting
- **404 "There isn't a GitHub Pages site here"**: Pages isn't enabled, or `index.html` isn't at the repo root. Make sure you uploaded the folder's *contents*, not the folder itself.
- **Domain check fails**: an old A record is still there, or DNS hasn't updated yet. Remove extra records and wait.
- **Custom domain setting disappears after a push**: the `CNAME` file is missing. Keep it in the repo root.
- **Fonts look plain**: this happens only when you open the file offline. Online, the fonts load from Google Fonts.

---

## Adding or updating terms

1. Edit `data/terms.json`:

   ```json
   {
     "id": "agent-harness",
     "t": "Agent Harness",
     "c": "Agent Infrastructure & Protocols",
     "l": "P",
     "s": "new",
     "d": "Two or three plain-English sentences…",
     "e": "A short example or analogy."
   }
   ```

   - `l` (level): `B` Beginner · `P` Practitioner · `A` Advanced
   - `s` (status): `new` · `hot` (Trending) · `est` (Established)
   - `c` must match a name in the `categories` list at the top of the file.
   - `id` must be unique. It becomes the shareable link, e.g. `skillvenue.com/#agent-harness`.
   - Update `"updated"` at the top to today's date.
2. Rebuild: `python3 build/build.py` (plain Python 3, no packages needed).
3. Commit and push (or upload the changed `index.html`, `sitemap.xml` and `data/terms.json` in the browser). The site updates in about a minute.

## Features
- Instant search across terms, definitions and examples (press `/` to focus)
- Filters for New in 2026, Trending, level and section, with an A→Z or by-section view
- A "What's inside" section grid, a term of the day, "Surprise me", and a copyable link for every term
- SEO: all content is in the page as static HTML, plus schema.org `DefinedTermSet` data, a sitemap and robots.txt
- Mobile-friendly, and no build dependencies
