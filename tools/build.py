# One-off generator for the static site. Output is plain HTML committed to the repo.
# Usage (from repo root): python3 tools/build.py .
import sys, os
from html import escape as e

OUT = sys.argv[1]
EMAIL = "zkaplan1103@gmail.com"
GH = "https://github.com/zkaplan1103/"
LI = "https://www.linkedin.com/in/zachary-kaplan-3bb703273"

P = [
 dict(slug="mcp-verify", title="mcp-verify", tag="Benchmarked hallucination detector", type="ai", year=2026,
  claim="A hallucination detector with a real benchmark behind it.",
  stat=("97.9%", "precision on 106 labeled cases"),
  links=[("GitHub", GH+"mcp-verify")],
  problem="AI drafts sound confident even when they are wrong. Checking every claim by hand is slow. Most detectors never prove they work. I wanted one that shows its numbers.",
  steps=[("Input", "You give it a source of truth and a draft to check."),
         ("Check", "Each claim in the draft is checked against the source."),
         ("Report", "Unsupported claims come back as JSON with a reason, the source fact checked, a category and a severity."),
         ("Confirm", "Reliability mode runs the check several times. It keeps the claims a majority agree on and moves unstable ones to an uncertain list.")],
  stats=[("97.9%", "precision"), ("99.1%", "recall"), ("106", "labeled cases"), ("4", "domains plus a red team set")],
  body="<p>It runs as a Python library or as an MCP server with one tool. As a server it can borrow the host's model through MCP sampling. That means no API key and no extra cost.</p><p>The eval suite travels with the detector. It has a 15 type hallucination taxonomy and an adversarial red team set. It runs in CI so accuracy can't slip before a release.</p>",
  stack=["Python", "Claude API", "MCP", "pytest", "GitHub Actions"],
  next="Every remaining failure is reviewed and written up in the benchmark doc. Next I want more domains and a bigger red team set."),
 dict(slug="bizbrief", title="BizBrief", tag="Serverless review intelligence pipeline", type="ai", year=2026,
  claim="Customer reviews in. A ranked weekly action brief out.",
  stat=("72%", "lower projected model spend"),
  links=[("Live demo", "https://zkaplan1103.github.io/Business-Brief/"), ("GitHub", GH+"Business-Brief")],
  img=("bizbrief.png", "BizBrief overview with a rating gauge, the weekly brief and the top action"),
  problem="Small business owners get a flood of reviews and no time to read them. They need to know what to fix this week. They also need the reviews that prove it.",
  steps=[("Ingest", "Reviews are grouped by business and by week."),
         ("Route", "A complexity score sends each batch to the cheapest Claude model that can handle it. Haiku, Sonnet or Opus."),
         ("Classify", "Claude tags recurring themes and sentiment and keeps the review evidence for each one."),
         ("Brief", "The top issues are ranked by impact. Each one gets a recommended action and a draft email.")],
  stats=[("72%", "lower projected spend"), ("36x", "cheaper than Opus on the eval batch"), ("14", "red team findings, 12 fixed"), ("3", "Lambda stages")],
  body="<p>Routing and prompt caching bring the projected cost from about 99 cents to 28 cents per thousand reviews.</p><p>The serverless version is built with AWS SAM. Dropping a file in S3 fires an ingest, analyze and brief Lambda chain that writes to DynamoDB. Failed runs land in an SQS dead letter queue with an alarm. The API key lives in Secrets Manager. Every role only gets the actions its handler calls.</p>",
  stack=["Python", "Claude API", "FastAPI", "React", "AWS SAM", "Lambda", "DynamoDB", "SQS"],
  next="The AWS stack is deployable but not deployed, since running it costs real money. The live demo uses simulated data for four fictional businesses."),
 dict(slug="policylens", title="PolicyLens", tag="Privacy policy Q&amp;A with citations", type="ai", year=2026,
  claim="Ask a privacy policy a question. Get the clause that answers it.",
  stat=("2,393", "clauses across 115 real policies"),
  links=[("GitHub", GH+"RAG_PRIVACY")],
  problem="Privacy policies are long and written by lawyers. People want a straight answer to a normal question. Does this app share my data with advertisers?",
  steps=[("Ingest", "115 real policies from the OPP-115 corpus are split into 2,393 labeled clauses."),
         ("Retrieve", "Hybrid vector and full text search plus a reranker return the top five clauses."),
         ("Answer", "Claude answers from those clauses only and cites each one it used."),
         ("Abstain", "If no clause clears the confidence floor, the app says the policy doesn't cover it.")],
  stats=[("115", "policies"), ("2,393", "clauses"), ("167", "golden Q&amp;A items"), ("157", "unit tests")],
  body="<p>Every citation traces back to a real clause ID and real text from the policy. The model is told not to use outside knowledge.</p><p>The production path runs on Supabase pgvector behind API Gateway and Lambda, set up with Terraform. CI runs faithfulness and abstention checks and blocks a change if either drops below its threshold.</p>",
  stack=["Python", "Claude API", "RAG", "pgvector", "Supabase", "Terraform", "AWS Lambda", "Ragas"],
  next="Two separate abstention paths keep it honest. One stops weak matches before the model runs. The other lets the model refuse when the clauses don't support an answer."),
 dict(slug="grant-navigator", title="Grant Navigator", tag="Multi-agent grant matching", type="ai", year=2026,
  claim="Grant matches for nonprofits, with a check that blocks made up claims.",
  stat=("100%", "precision and recall on 31 cases"),
  links=[("GitHub", GH+"grant-finder")],
  problem="Nonprofits chase funding across grants.gov, foundation sites and spreadsheets. It is slow work. One false eligibility claim can get an organization barred. The project started after the EPA cancelled Solar for All in August 2025 and solar nonprofits had to replace that money fast.",
  steps=[("Profile", "A nonprofit enters its funding focus and details."),
         ("Discover", "Live grants.gov search runs alongside a vetted list of foundation and state sources."),
         ("Match", "A Sonnet agent scores fit and ranks every result with a cited reason."),
         ("Verify", "A drafter writes application text. An Opus verify agent sends back anything unsupported. Holdouts go to a person.")],
  stats=[("100%", "precision"), ("100%", "recall"), ("31", "benchmark cases"), ("3", "agents, one bounded loop")],
  body="<p>Discovery is a tool, not an agent. Source trust is a config list vetted ahead of time. The agent loop is written by hand on the Anthropic SDK with no framework.</p><p>The verify step runs on the strongest model on purpose. A cheap model waves hallucinations through.</p>",
  stack=["Python", "Claude API", "FastAPI", "React", "TypeScript", "SQLite"],
  next="The curated sources only cover solar and clean energy for now. Any other focus still gets full federal results."),
 dict(slug="panel-cv-leakage", title="Panel CV &amp; Data Leakage", tag="Econometrics and ML research", type="data", year=2025,
  claim="A popular cross validation tool was quietly training on the future.",
  stat=("254,062", "rows of daily box office data"),
  links=[("GitHub", GH+"panel-cv-leakage"), ("Paper", GH+"panel-cv-leakage/blob/main/paper/panel-cv-strategies-paper.pdf")],
  problem="On panel data the split itself can leak answers. The same movie can land in train and test. The model can also train on dates after the test window. Either way the score looks better than it should.",
  steps=[("Clean", "Merged two sources into 254,062 daily rows for 3,400 movies and kept the group structure intact."),
         ("Audit", "Asserted on every fold. GroupTimeSeriesSplit was training on 2020 data against a 2006 test window."),
         ("Fix", "Wrote a splitter that sorts groups by date instead of by row order."),
         ("Benchmark", "Tuned linear regression, decision trees and XGBoost across four validation strategies.")],
  stats=[("254,062", "rows"), ("3,400", "movies"), ("4", "CV strategies"), ("0", "leaks in the fixed splitter")],
  body="<p>The community splitter orders groups by where they first appear in the array. It only works if the data was already sorted by date. Nothing warns you when it isn't.</p><p>Once both leaks are closed, test error rises and fold variance widens. That is the honest number. It's the one a forecast should use.</p>",
  stack=["Python", "pandas", "scikit-learn", "XGBoost", "Jupyter"],
  next="This was my Econ 167 final at Pomona. The repo includes a leakage checker that works on any splitter."),
 dict(slug="air-labs-gtm", title="Air Labs GTM Pipeline", tag="Lead processing case study", type="data", year=2026,
  claim="Messy inbound leads in. A clean Salesforce payload out.",
  stat=("89", "clean leads scored from 100 raw rows"),
  links=[("GitHub", GH+"AIR_LABS_GTM_CASE-STUDY")],
  problem="Inbound lead lists are messy. Bad emails, duplicates, missing names and free text company fields. Sales can't prioritize until someone cleans and scores them.",
  steps=[("Ingest", "Parse the CSV and validate every row with Zod."),
         ("Normalize", "Clean emails, phones, dates and companies. Drop bad emails and dedupe."),
         ("Enrich", "Call a mock company data API with retries, backoff and a cache."),
         ("Score", "26 JSON rules give each lead a score and a hot, warm or cold tier.")],
  stats=[("100", "raw leads"), ("89", "after cleaning and dedup"), ("15", "hot leads"), ("26", "scoring rules")],
  body="<p>Scoring lives in a JSON file, so sales ops can change rules without touching code. Six runtime checks guard against silent data loss and stop the run if any one fails.</p><p>The output is a Salesforce Bulk API payload plus a flagged list for human review.</p>",
  stack=["TypeScript", "Node", "Zod", "Vitest", "Salesforce Bulk API"],
  next="The written case study rebuilds what a production go to market pipeline could look like. It also maps how this batch job would grow into one."),
 dict(slug="water-polo-playbook", title="Water Polo Playbook", tag="Coaching app for animated plays", type="apps", year=2026,
  claim="Plays that move, built for the team I coach.",
  stat=("3", "platforms. iPad, phone and web"),
  links=[("Live app", "https://zkaplan1103.github.io/water-polo-playbook/"), ("GitHub", GH+"water-polo-playbook")],
  img=("water-polo-playbook.png", "Playbook editor showing a 6on5 play with every move drawn"),
  problem="Our plays lived on a whiteboard. Players saw them once and forgot them. I wanted one place where the team could watch every play move step by step.",
  steps=[("Set up", "Pick a half or full pool board drawn to scale and a formation like 6v6 or 6on5."),
         ("Build", "Move players slide by slide. Add pass lanes, shot lines and notes."),
         ("Play", "The app animates every cap and the ball between slides."),
         ("Present", "Present mode loops the play fullscreen on a TV or an iPad.")],
  stats=[("3", "platforms"), ("4", "sample plays built in"), ("0", "accounts or servers"), (".pptx", "export with speaker notes")],
  body="<p>Plays save on the device. There is no account or server. A play exports to PowerPoint with editable shapes and speaker notes, so a coach can drop it into a team meeting.</p><p>I use it with the boys team at The Hill School. We build new plays with the head coach and run them in practice from the app.</p>",
  stack=["Expo", "React Native", "TypeScript", "SVG", "GitHub Actions"],
  next="Folders, undo, light and dark themes and drag and drop are all in. Next is sharing a play by link."),
 dict(slug="terrapin-rewards", title="Terrapin Rewards", tag="Job. Multi-tenant loyalty platform", type="apps", year=2025,
  claim="One loyalty platform for a group of local businesses.",
  stat=("11", "months leading full stack development"),
  links=[("Live site", "https://terrapinrewards.netlify.app")],
  problem="Local businesses wanted a loyalty program without each one running its own system. Customers wanted one place to check in and collect points.",
  steps=[("Check in", "Customers scan a QR code at the counter."),
         ("Earn", "Points build toward rewards that each business sets."),
         ("Isolate", "Row level security in PostgreSQL means each business only sees its own data."),
         ("Track", "Real time dashboards on the Square API show engagement and retention.")],
  stats=[("11", "months"), ("1", "platform, many businesses"), ("RLS", "per business data isolation"), ("Live", "Square analytics")],
  body="<p>I led full stack development from January to November 2025. I met regularly with the business owners and turned their requests into shipped features.</p>",
  stack=["React 19", "TypeScript", "Supabase", "PostgreSQL", "Square API"],
  next="This was client work, so the code is private. The live site is public."),

 dict(slug="cat-kingdom", title="Cat Kingdom", tag="2D platformer in Unity", type="games", year=2024,
  claim="Four cat heroes. Swap between them to clear each level.",
  stat=("4", "playable cats, each with its own move"),
  links=[("Play on itch.io", "https://zkaplan1103.itch.io/cat-kingdom")],
  problem="Our game development midterm at DIS asked for a full 2D platformer. We wanted the puzzle to be picking the right character, not just jumping well.",
  steps=[("Story", "A story intro sets up the kingdom before the first level."),
         ("Swap", "Switch between four cats mid level. One rolls, one attacks, one double jumps and one flies."),
         ("Clear", "Three levels built so each section needs the right cat at the right time."),
         ("Finish", "A final scene closes out the story.")],
  stats=[("4", "playable cats"), ("3", "levels"), ("2", "person team"), ("0", "downloads needed")],
  body="<p>I built it with a teammate in Unity and C#. We wrote the character swap, movement and level logic ourselves. The art comes from third party sprite packs.</p>",
  stack=["Unity", "C#", "WebGL"],
  next="I rebuilt it for WebGL in 2026 so it plays in the browser with no download."),
 dict(slug="space-race", title="Space Race", tag="Gravity flipping platformer in Unity", type="games", year=2024,
  claim="A platformer where the world turns around you.",
  stat=("10", "levels with portals and a level select"),
  links=[("Play on itch.io", "https://zkaplan1103.itch.io/space-race"), ("GitHub", "https://github.com/GAMEDEVMIDTERM01/GameDevFinal")],
  img=("space-race.png", "Space Race title screen with a rover and a dotted path to a planet"),
  problem="For our final we wanted one mechanic that changes how every level reads. We picked rotation. Hit certain points and the whole world turns, so a wall can become the floor.",
  steps=[("Run", "Move and jump through a 2D level."),
         ("Flip", "Hit a trigger and the world rotates around the player."),
         ("Portal", "Portals send you across the map."),
         ("Select", "A level select lets you jump into any of the ten levels.")],
  stats=[("10", "levels"), ("1", "core mechanic"), ("2", "person team"), ("0", "downloads needed")],
  body="<p>I built it with a teammate in Unity and C#. Every level is designed around the rotation, so the same room plays differently once it turns.</p>",
  stack=["Unity", "C#", "WebGL"],
  next="This was our final project at DIS. I rebuilt it for WebGL in 2026 so it plays in the browser."),
]

TYPES = {"ai": ("AI &amp; LLMs", "blue"), "data": ("Data &amp; Research", "sage"), "apps": ("Apps &amp; Full Stack", "blush"), "games": ("Games", "lilac")}

def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;700&display=swap">
<link rel="stylesheet" href="/style.css">
<script src="/main.js" defer></script>
</head>
<body>
"""

def nav(cur):
    items = [("Work", "/work/"), ("CV", "/cv/"), ("Email", f"mailto:{EMAIL}")]
    lis = "".join(f'<li><a href="{h}"{" aria-current=page" if n == cur else ""}>{n}</a></li>' for n, h in items)
    return f'<div class="wrap">\n<header class="top"><a class="logo" href="/">Zachary Kaplan</a><nav aria-label="Main"><ul>{lis}</ul></nav></header>\n<main>\n'

def foot():
    return f"""</main>
<footer class="reveal">
  <p class="eyebrow">Get in touch</p>
  <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
  <div class="foot"><a href="{LI}">LinkedIn ↗</a><a href="https://github.com/zkaplan1103">GitHub ↗</a><a href="/cv/">CV</a><a href="/Zachary_Kaplan-Resume.pdf">Resume PDF</a></div>
</footer>
</div>
</body>
</html>
"""

def tags(xs, cls=""): return f'<ul class="tags {cls}">' + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"

def card(p, i, cls=""):
    label, color = TYPES[p["type"]]
    n, cap = p["stat"]
    return f"""<a class="card feature {color} reveal {cls}" href="/work/{p['slug']}/" data-type="{p['type']}">
  <span class="meta">{i:02d} · {label}</span>
  <h3>{p['title']}</h3>
  <p>{p['tag']}</p>
  <div><div class="stat">{n}</div><p>{cap}</p></div>
  {tags(p['stack'][:4])}
  <span class="go">Read walkthrough</span>
</a>"""

def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w") as f: f.write(html)

# Home. Staggered layout.
sel = [p for p in P if p["slug"] in ("mcp-verify", "bizbrief")]
home = head("Zachary Kaplan", "Zachary Kaplan builds software that solves real problems.") + nav("") + f"""
<section class="hero stair">
  <div style="grid-column:1/-1" class="reveal">
    <p class="eyebrow short">Software engineer</p>
    <h1 class="name"><span>Zachary</span><span>Kaplan</span></h1>
  </div>
  <div class="hero-bio reveal">
    <p class="lede">I build software that solves real problems.</p>
    <p class="muted" style="margin-top:1em">Backend systems, mobile apps, data pipelines and AI tools. I like messy problems. I find the part that matters, build the fix and make sure it holds up.</p>
  </div>
  <div class="hero-now reveal">
    <p class="eyebrow">Now</p>
    <p><b>Lead backend developer</b> at <a href="https://www.umee.social">Umee Social</a></p>
    <p><b>Assistant water polo coach</b> at The Hill School</p>
  </div>
</section>

<section class="sec" id="work">
  <p class="eyebrow reveal">Selected work</p>
  <div class="stair">
    {card(sel[0], 1, "sel-a")}
    {card(sel[1], 2, "sel-b")}
    <div class="sel-cta reveal"><a class="cta" href="/work/">See all {len(P)} projects →</a></div>
  </div>
</section>

<section class="sec">
  <p class="eyebrow reveal">About</p>
  <div class="stair">
    <div class="item about-1 reveal"><span class="n">01</span><h3>Water polo</h3><p class="muted">I played four years at Pomona-Pitzer and won a Division III national title my first year. Now I coach the boys team at The Hill School, where I went to high school.</p></div>
    <div class="item about-2 reveal"><span class="n">02</span><h3>Building</h3><p class="muted">I like building things I want to exist. The playbook app started because our plays lived on a whiteboard. I've also made <a href="/work/?type=games">games in Unity and C#</a>.</p></div>
    <div class="item about-3 reveal"><span class="n">03</span><h3>Tradeoffs</h3><p class="muted">The economics side shows up in how I build. I think about cost per run and whether the data actually supports the claim.</p></div>
  </div>
</section>

<section class="sec">
  <p class="eyebrow reveal">Education</p>
  <div class="stair">
    <div class="edu-a reveal">
      <h2>Pomona<br>College</h2>
      <p class="lede muted" style="margin-top:.6em">B.A. Computer Science. Minor in Economics.</p>
    </div>
    <ul class="facts edu-b reveal">
      <li><b>3.78</b><span>GPA</span></li>
      <li><b>4x</b><span>Academic All-American</span></li>
      <li><b>2021</b><span>D3 water polo national champion</span></li>
    </ul>
  </div>
</section>
""" + foot()
write("index.html", home)

# Work index. Neat grid.
chips = '<button type="button" data-filter="all" aria-pressed="true">All <span class="count">' + str(len(P)) + '</span></button>' + "".join(
    f'<button type="button" data-filter="{k}" aria-pressed="false">{lab} <span class="count">{sum(p["type"] == k for p in P)}</span></button>'
    for k, (lab, _) in TYPES.items())
work = head("Work · Zachary Kaplan", "Projects by Zachary Kaplan. AI systems, data research and apps.") + nav("Work") + f"""
<section class="hero reveal">
  <p class="eyebrow short">{len(P)} projects</p>
  <h1 class="page">Work</h1>
  <p class="lede muted prose" style="margin-top:.5em">Everything here is finished and linked. Pick a type or open any card for the full walkthrough.</p>
</section>
<div class="filters" role="group" aria-label="Filter projects by type">{chips}</div>
<section class="grid g2" aria-label="Projects">
{chr(10).join(card(p, i + 1) for i, p in enumerate(P))}
</section>
""" + foot()
write("work/index.html", work)

# Walkthroughs. Neat.
for i, p in enumerate(P):
    label, color = TYPES[p["type"]]
    prev_p, next_p = P[i - 1], P[(i + 1) % len(P)]
    links = "".join(f'<a class="btn" href="{h}">{n} ↗</a>' for n, h in p["links"])
    steps = "".join(f'<div class="step reveal"><span class="n">0{j+1}</span><b>{t}</b><p>{d}</p></div>' for j, (t, d) in enumerate(p["steps"]))
    nums = "".join(f'<div><b>{n}</b><span>{c}</span></div>' for n, c in p["stats"])
    img = f'<section class="sec reveal"><img class="shot" src="/img/{p["img"][0]}" alt="{p["img"][1]}" loading="lazy"></section>' if "img" in p else ""
    page = head(f"{p['title'].replace('&amp;', '&')} · Zachary Kaplan", p["claim"]) + nav("Work") + f"""
<section class="hero reveal">
  <p class="eyebrow short">{label} · {p['year']}</p>
  <h1 class="page">{p['title']}</h1>
  <p class="lede prose" style="margin-top:.6em">{p['claim']}</p>
  <div class="links">{links}</div>
</section>
<section class="sec grid g-side reveal">
  <p class="eyebrow">The problem</p>
  <p class="lede prose">{p['problem']}</p>
</section>
{img}
<section class="sec"><p class="eyebrow reveal">How it works</p><div class="grid g4">{steps}</div></section>
<section class="sec reveal"><p class="eyebrow">Results</p><div class="nums">{nums}</div></section>
<section class="sec grid g-side reveal">
  <p class="eyebrow">Details</p>
  <div>
    <div class="prose muted">{p['body']}</div>
    <p class="prose muted" style="margin-top:.8em">{p['next']}</p>
    <div style="margin-top:24px">{tags(p['stack'], 'quiet-tags')}</div>
  </div>
</section>
<nav class="sec grid g2 pager" aria-label="More projects">
  <a class="card {TYPES[prev_p['type']][1]} reveal" href="/work/{prev_p['slug']}/"><span class="feature"><span class="meta">← Previous</span></span><h3>{prev_p['title']}</h3></a>
  <a class="card next {TYPES[next_p['type']][1]} reveal" href="/work/{next_p['slug']}/"><span class="feature"><span class="meta">Next →</span></span><h3>{next_p['title']}</h3></a>
</nav>
<div class="sec reveal"><a class="cta" href="/work/">← All work</a></div>
""" + foot()
    write(f"work/{p['slug']}/index.html", page)

# CV. Neat.
def role(org, url, title, dates, bullets):
    o = f'<a href="{url}">{org}</a>' if url else org
    return f'<article class="role"><header><h3>{o}</h3><span class="when">{dates}</span></header><p class="title">{title}</p><ul>' + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></article>"

cv = head("CV · Zachary Kaplan", "CV for Zachary Kaplan, software engineer.") + nav("CV") + f"""
<section class="hero reveal">
  <p class="eyebrow short">Curriculum vitae</p>
  <h1 class="page">Zachary Kaplan</h1>
  <p class="lede muted" style="margin-top:.6em">Software engineer. I build backend systems, apps, data pipelines and AI tools.</p>
  <div class="links no-print"><a class="btn" href="/Zachary_Kaplan-Resume.pdf" download>Download PDF ↓</a><a class="btn alt" href="mailto:{EMAIL}">Email ↗</a><a class="btn alt" href="{LI}">LinkedIn ↗</a></div>
</section>
<section class="sec grid g-side reveal"><p class="eyebrow">Experience</p><div>
{role("Umee Social", "https://www.umee.social", "Backend Developer", "Oct 2026 to now", [
  "Lead backend developer improving the admin panel and community health board.",
  "Build frontend features for the Umee mobile app in Flutter.",
  "Work across AWS services to support and extend the app's backend."])}
{role("The Hill School", "", "Assistant Boys Water Polo Coach", "Aug 2025 to now", [
  'Built a <a href="/work/water-polo-playbook/">playbook app</a> where coaches draw and animate plays step by step, giving the team one place to learn strategy.',
  "Developed new drills and game strategies with the head coach and implemented them in practice through the playbook.",
  "Led drills and small-group work, tailoring sessions to player skill level and delivering one-on-one feedback."])}
{role("Terrapin Rewards", "https://terrapinrewards.netlify.app", "Full-Stack Software Engineer", "Jan 2025 to Nov 2025", [
  "Led full-stack development of a multi-tenant loyalty platform in React 19, TypeScript and Supabase.",
  "Architected secure PostgreSQL schemas with row-level security to isolate client data, integrating real-time Square API analytics dashboards to track engagement.",
  "Ran recurring sessions with business owners to translate operational needs into design and product decisions, shipping custom-requested features."])}
{role("Mindsprout", "https://mindsprout.ai", "Backend Software Engineer Intern", "Dec 2024 to Mar 2025", [
  "Integrated Claude 3.5 API into a production backend to automate core user workflows, eliminating manual processing bottlenecks for end users.",
  "Deployed containerized infrastructure with Docker to support reliable backend model serving in production."])}
</div></section>
<section class="sec grid g-side reveal"><p class="eyebrow">Projects</p>
<div class="rows">{"".join(f'<a href="/work/{p["slug"]}/"><h3>{p["title"]}</h3><span>{p["tag"]} →</span></a>' for p in P)}</div></section>
<section class="sec grid g-side reveal"><p class="eyebrow">Education</p><div>
<article class="role" style="border-top:0;padding-top:0"><header><h3>Pomona College</h3><span class="when">Claremont, CA</span></header><p class="title">B.A. Computer Science, Minor in Economics</p>
<ul><li>3.78 GPA.</li><li>Academic All-American 2021 to 2024.</li><li>Division III Men's Water Polo National Champion 2021. Pomona-Pitzer 2021 to 2024.</li></ul></article>
</div></section>
<section class="sec grid g-side reveal"><p class="eyebrow">Skills</p><dl class="skills">
<dt>Languages</dt><dd>Python, TypeScript, JavaScript, Dart, SQL</dd>
<dt>Data &amp; Analytics</dt><dd>SQL, Pandas, Scikit-learn, XGBoost, ETL, Data Cleaning &amp; Validation, Dashboards &amp; Reporting</dd>
<dt>Full Stack &amp; Backend</dt><dd>React, Next.js, Flutter, FastAPI, Supabase, PostgreSQL, PostGIS, Tailwind</dd>
<dt>Cloud &amp; Infra</dt><dd>AWS (Lambda, S3, DynamoDB, SQS), SAM, Terraform, Docker, CI/CD</dd>
<dt>AI &amp; Automation</dt><dd>Claude API, OpenAI API, MCP, Multi-Agent Workflows, RAG, Evaluation Harnesses</dd>
<dt>Business</dt><dd>Salesforce (Bulk API), Square API, Lead Scoring, Cost Modeling, Competitive Analysis</dd>
</dl></section>
""" + foot()
write("cv/index.html", cv)

write("404.html", head("Not found · Zachary Kaplan", "Page not found.") + nav("") + '<section class="hero"><h1 class="page">404</h1><p class="lede muted" style="margin-top:.5em">That page doesn\'t exist.</p><div class="links"><a class="btn" href="/">Go home</a></div></section>' + foot())

write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1B1A18"/><text x="32" y="43" text-anchor="middle" font-family="Century Gothic,Futura,sans-serif" font-weight="700" font-size="28" fill="#C9D9EA">ZK</text></svg>')

# ponytail: self-check. Every internal link resolves to a generated file.
import re, glob
for f in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    for href in re.findall(r'href="(/[^"#?]*)', open(f).read()):
        target = os.path.join(OUT, href.lstrip("/"))
        assert os.path.exists(target if not href.endswith("/") else target + "index.html"), (f, href)
    assert "water-polo-playbook-pomona" not in open(f).read(), f
print("built", len(glob.glob(os.path.join(OUT, '**/*.html'), recursive=True)), "pages, internal links OK")
