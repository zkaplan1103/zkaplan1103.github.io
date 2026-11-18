# Generator for the static site. Output is plain HTML committed to the repo.
# Usage (from repo root): python3 tools/build.py .
# Each project lists its own sections, so walkthroughs follow how the project actually went.
import sys, os, re, glob

OUT = sys.argv[1]
EMAIL = "zkaplan1103@gmail.com"
GH = "https://github.com/zkaplan1103/"
LI = "https://www.linkedin.com/in/zachary-kaplan-3bb703273"
ITCH = "https://zkaplan1103.itch.io/"

TYPES = {"ai": ("AI &amp; LLMs", "blue"), "data": ("Data &amp; Research", "sage"),
         "apps": ("Apps &amp; Full Stack", "blush"), "games": ("Games", "lilac")}

# Section helpers. Each returns a tuple the renderer understands.
def text(label, html, big=False): return ("text", label, html, big)
def steps(label, items): return ("steps", label, items)
def nums(label, items): return ("nums", label, items)
def table(label, head, rows, note=""): return ("table", label, head, rows, note)
def items(label, rows): return ("items", label, rows)
def img(src, alt): return ("img", src, alt)

P = [
 dict(slug="mcp-verify", title="mcp-verify", tag="Benchmarked hallucination detector", type="ai", year=2026,
  claim="Checks an AI draft against a source and flags every claim the source doesn't support.",
  stat=("97.9%", "precision on 106 labeled cases"),
  links=[("GitHub", GH+"mcp-verify")],
  stack=["Python", "Claude API", "MCP", "pytest", "GitHub Actions"],
  sections=[
   text("The problem", "Language models write confident text that is sometimes wrong. If that text goes to a customer, someone has to check every claim. I wanted a checker I could trust, so I built one and measured how often it's right.", big=True),
   text("What it does", "<p>You pass in a source of truth and a draft. It returns each claim the source doesn't back up. Every flag comes with a reason, the fact it checked, a category and a severity.</p><p>It works as a Python library or as an MCP server with one tool. As a server it can use the host's own model through MCP sampling, so it runs without an API key. A reliability mode runs the check several times and only keeps the claims most runs agree on.</p>"),
   nums("Results", [("97.9%", "precision"), ("99.1%", "recall"), ("98.5%", "F1"), ("106", "labeled cases")]),
   items("The benchmark", [("106 cases", "Labeled drafts across 4 domains."),
                           ("Red team set", "Adversarial cases written to slip past the checker."),
                           ("15 types", "A taxonomy of the ways a draft can be wrong."),
                           ("3 runs", "Scores are averaged over three runs with 95% confidence intervals."),
                           ("CI gate", "The suite runs on every change so accuracy can't quietly drop.")]),
   text("Notes", "Every miss that's left is written up in the benchmark doc along with why it happened."),
  ]),
 dict(slug="bizbrief", title="BizBrief", tag="Serverless review intelligence pipeline", type="ai", year=2026,
  claim="Turns a week of customer reviews into a short list of what to fix.",
  stat=("72%", "lower projected model spend"),
  links=[("Live demo", "https://zkaplan1103.github.io/Business-Brief/"), ("GitHub", GH+"Business-Brief")],
  stack=["Python", "Claude API", "FastAPI", "React", "AWS SAM", "Lambda", "DynamoDB", "SQS"],
  sections=[
   text("The problem", "Small business owners get more reviews than they can read. The useful part is usually a few repeated complaints. I wanted something that pulls those out every week and backs each one with the reviews that prove it.", big=True),
   img("bizbrief.png", "BizBrief overview with a rating gauge, the weekly brief and the top action"),
   steps("How it works", [("Ingest", "Reviews come in grouped by business and week."),
                          ("Route", "Each batch is scored on length, star spread and vocabulary. Then it goes to the cheapest model that can handle it."),
                          ("Analyze", "Claude tags themes and sentiment and keeps the reviews behind each one."),
                          ("Brief", "The top issues are ranked by impact. Each gets a recommended action and a draft reply.")]),
   table("Picking models", ["Model", "Cost per run", "Label F1"],
         [["Haiku", "$0.0045", "0.60"], ["Sonnet", "$0.0169", "0.18"], ["Opus", "$0.0900", "0.50"]],
         "On the eval batch Haiku scored highest at the lowest cost. Sonnet found the right themes but worded its labels differently from the answer key. That's why most batches route to Haiku."),
   nums("Cost per 1,000 reviews", [("$0.99", "Sonnet for everything"), ("$0.34", "with routing"), ("$0.28", "with routing and caching"), ("72%", "saved")]),
   text("AWS version", "<p>I also built an event-driven version on AWS with SAM. Uploading a file to S3 starts a chain of Lambda functions that ingest, analyze and write the brief to DynamoDB. Failed runs go to an SQS dead letter queue with an alarm.</p><p>It reuses the same routing, caching and retry code as the local version. It passes validation but isn't deployed, since running it costs money. The live demo uses simulated data for four made up businesses.</p>"),
   text("Security", "I red-teamed the API before calling it done. That turned up 14 findings. I fixed 12, and the other 2 were low risk. The fixes included per-IP rate limits, API key auth with lockouts, path checks and a cap on request size."),
  ]),
 dict(slug="policylens", title="PolicyLens", tag="Privacy policy Q&amp;A with citations", type="ai", year=2026,
  claim="Answers questions about a privacy policy and cites the exact clause it used.",
  stat=("2,393", "clauses across 115 real policies"),
  links=[("GitHub", GH+"RAG_PRIVACY")],
  stack=["Python", "Claude API", "RAG", "pgvector", "Supabase", "Terraform", "AWS Lambda", "Ragas"],
  sections=[
   text("The problem", "Nobody reads privacy policies. They're long and written by lawyers. I wanted to ask a normal question, like whether an app shares my data with advertisers, and get a short answer I could check.", big=True),
   steps("How it works", [("Ingest", "115 real policies from the OPP-115 corpus are split into 2,393 labeled clauses."),
                          ("Retrieve", "The question is matched against that policy with vector and keyword search, then reranked. The top five clauses come back."),
                          ("Answer", "Claude answers from those five clauses only and cites each one.")]),
   text("When it says no", "<p>The hardest part was getting it to admit when a policy doesn't cover something. There are two checks. If no clause scores high enough, it stops before calling the model. If the model reads the clauses and they don't support an answer, it says so instead of guessing.</p>"),
   nums("Evaluation", [("167", "golden questions"), ("30", "of them unanswerable on purpose"), ("0.80", "faithfulness floor in CI"), ("157", "unit tests")]),
   text("Production", "The production version runs on Supabase pgvector behind API Gateway and Lambda, set up with Terraform. CI runs the eval and blocks a change if faithfulness or abstention accuracy drops below its floor."),
  ]),
 dict(slug="grant-navigator", title="Grant Navigator", tag="Multi-agent grant matching", type="ai", year=2026,
  claim="Matches a nonprofit to grants and drafts the application text, with a check that blocks false claims.",
  stat=("100%", "precision and recall on 31 cases"),
  links=[("GitHub", GH+"grant-finder")],
  stack=["Python", "Claude API", "FastAPI", "React", "TypeScript", "SQLite"],
  sections=[
   text("The problem", "Nonprofits find funding by digging through grants.gov, foundation sites and spreadsheets. It's slow. One false eligibility claim can get an organization barred. I started this after the EPA cancelled Solar for All in August 2025 and solar nonprofits had to replace that money quickly.", big=True),
   steps("How it works", [("Profile", "The nonprofit describes itself and what it needs money for."),
                          ("Search", "A live grants.gov search runs next to a hand-vetted list of foundation and state programs."),
                          ("Match", "A Sonnet agent scores how well each grant fits and explains why."),
                          ("Draft", "Sonnet writes application boilerplate for the strong matches."),
                          ("Verify", "Opus checks every claim in the draft. Anything unsupported goes back for a rewrite or gets flagged for a person.")]),
   nums("Verify benchmark", [("100%", "precision"), ("100%", "recall"), ("31", "test cases"), ("3", "difficulty tiers")]),
   items("Choices I made", [("No framework", "The agent loop is written by hand on the Anthropic SDK."),
                            ("Search is a tool", "Only the steps that need judgment are agents."),
                            ("Best model verifies", "A cheaper model let made up claims through."),
                            ("Vetted sources", "Which sites to trust is decided ahead of time in a config file.")]),
   text("Limits", "The hand-vetted sources only cover solar and clean energy for now. Any other focus still gets the full federal results."),
  ]),
 dict(slug="panel-cv-leakage", title="Panel CV &amp; Data Leakage", tag="Econometrics and ML research", type="data", year=2025,
  claim="I found a popular cross validation splitter training models on future data.",
  stat=("254,062", "rows of daily box office data"),
  links=[("GitHub", GH+"panel-cv-leakage"), ("Paper", GH+"panel-cv-leakage/blob/main/paper/panel-cv-strategies-paper.pdf")],
  stack=["Python", "pandas", "scikit-learn", "XGBoost", "Jupyter"],
  sections=[
   text("The question", "For my Econ 167 final I wanted to see how much the choice of cross validation changes results on panel data. The data was daily box office numbers for 3,400 movies from 1999 to 2020.", big=True),
   text("What I found", "<p>The community GroupTimeSeriesSplit sorts groups by where they first show up in the data, not by date. If the data isn't already sorted by date, it trains on the future and still reports a good score.</p><p>I caught it because I checked every fold. One fold trained on data through 2020 and tested on 2006.</p>"),
   text("The fix", "I wrote a version that takes the dates directly and sorts by them. I also wrote a checker that tests any splitter for both kinds of leakage."),
   table("Results", ["CV strategy", "What leaks", "XGBoost MSE"],
         [["KFold", "Same movie and future dates", "0.824"], ["GroupKFold", "Future dates", "0.748"],
          ["GroupTimeSeriesSplit", "Some future dates", "0.798"], ["My fixed splitter", "Nothing", "0.775"]],
         "The leaky splits looked more stable than they should. Once both leaks are closed the error rises and varies more between folds. That number is less flattering, but it's the honest one to use for a forecast."),
   nums("The data", [("254,062", "rows"), ("3,400", "movies"), ("3", "models"), ("4", "CV strategies")]),
  ]),
 dict(slug="air-labs-gtm", title="Air Labs GTM Pipeline", tag="Lead processing case study", type="data", year=2026,
  claim="Cleans, enriches and scores a messy list of inbound leads for Salesforce.",
  stat=("89", "clean leads scored from 100 raw rows"),
  links=[("GitHub", GH+"AIR_LABS_GTM_CASE-STUDY")],
  stack=["TypeScript", "Node", "Zod", "Vitest", "Salesforce Bulk API"],
  sections=[
   text("The brief", "This started as a take-home for a GTM engineering role at Air. The task was to turn a messy CSV of inbound leads into something sales could use. I built the pipeline and wrote a case study on how it would run in production.", big=True),
   steps("The pipeline", [("Ingest", "Parse the CSV and check every row against a Zod schema."),
                          ("Normalize", "Clean emails, phones, dates and company names. Drop bad emails and remove duplicates."),
                          ("Enrich", "Look up each company through a mock data API with retries and a cache."),
                          ("Score", "26 rules in a JSON file give each lead a score and a hot, warm or cold tier."),
                          ("Output", "Write a Salesforce Bulk API payload and a separate list for human review.")]),
   nums("The run", [("100", "raw leads"), ("89", "after cleaning"), ("15", "hot"), ("43", "warm")]),
   items("The case study", [("00", "Who Air is and why I picked them."),
                            ("01", "What the data stands for and the question it answers."),
                            ("02", "A simulated version of the full go to market pipeline."),
                            ("03", "What the run showed and what follows from it."),
                            ("04", "What it would take to run this in production.")]),
   text("Notes", "Scoring rules live in JSON so sales ops can change them without touching code. Six checks run at the end and stop the job if any lead goes missing."),
  ]),
 dict(slug="water-polo-playbook", title="Water Polo Playbook", tag="Coaching app for animated plays", type="apps", year=2026,
  claim="An app I built for the team I coach to draw plays and watch them move.",
  stat=("3", "platforms. iPad, phone and web"),
  links=[("Live app", "https://zkaplan1103.github.io/water-polo-playbook/"), ("GitHub", GH+"water-polo-playbook")],
  stack=["Expo", "React Native", "TypeScript", "SVG", "GitHub Actions"],
  sections=[
   text("Why I built it", "Our plays lived on a whiteboard. Players saw them once in practice and forgot them. I wanted a place where the team could watch every play move step by step, on whatever device they had.", big=True),
   img("water-polo-playbook.png", "Playbook editor showing a 6on5 play with every move drawn"),
   items("What it does", [("Boards to scale", "Half and full pool with the 2, 5 and 6 meter lines."),
                          ("Formations", "6v6, 6on5, 5on6 and counterattack setups built in."),
                          ("Slides", "Move players slide by slide and the app animates between them."),
                          ("Present mode", "Loops a play fullscreen on a TV or an iPad."),
                          ("Lines and notes", "Pass lanes, shot lines and notes on any slide."),
                          ("PowerPoint export", "Editable shapes with speaker notes.")]),
   text("How we use it", "We build new plays with the head coach and walk the team through them in present mode. Everything saves on the device, so there's no account to set up."),
  ]),
 dict(slug="terrapin-rewards", title="Terrapin Rewards", tag="Job. Multi-tenant loyalty platform", type="apps", year=2025,
  claim="A loyalty platform I built for a group of local businesses.",
  stat=("11", "months leading full stack development"),
  links=[("Live site", "https://terrapinrewards.netlify.app")],
  stack=["React 19", "TypeScript", "Supabase", "PostgreSQL", "Square API"],
  sections=[
   text("The job", "I led full stack development at Terrapin Rewards from January to November 2025. The goal was one loyalty system that several local businesses could share. Customers check in with a QR code and earn points toward rewards each business sets.", big=True),
   items("What I built", [("Shared platform", "One React and Supabase app that serves every business."),
                          ("Data isolation", "PostgreSQL row-level security so each business only sees its own customers."),
                          ("Analytics", "Real time dashboards on the Square API for engagement and retention."),
                          ("Custom features", "Built from requests that came out of regular meetings with the owners.")]),
   text("Notes", "This was client work, so the code is private. The live site is public."),
  ]),
 dict(slug="cat-kingdom", title="Cat Kingdom", tag="2D platformer in Unity", type="games", year=2024,
  claim="A 2D platformer where you switch between four cats to get through each level.",
  stat=("4", "playable cats, each with its own move"),
  links=[("Play on itch.io", ITCH+"cat-kingdom")],
  stack=["Unity", "C#", "WebGL"],
  sections=[
   text("About the game", "I made it with a teammate for our game development midterm at DIS. There are three levels with a story intro and a final scene.", big=True),
   text("How it plays", "You can swap cats at any point in a level. Each one has a single move. One rolls, one attacks, one double jumps and one flies."),
   text("Making it", "We wrote it in C# in Unity. The art comes from third party sprite packs. In 2026 I rebuilt it for WebGL so it plays in the browser."),
  ]),
 dict(slug="space-race", title="Space Race", tag="Gravity flipping platformer in Unity", type="games", year=2024,
  claim="A 2D platformer where the world rotates around you.",
  stat=("10", "levels with portals and a level select"),
  links=[("Play on itch.io", ITCH+"space-race"), ("GitHub", "https://github.com/GAMEDEVMIDTERM01/GameDevFinal")],
  stack=["Unity", "C#", "WebGL"],
  sections=[
   text("About the game", "I made it with a teammate as our game development final at DIS. When you hit certain points the whole level turns, so a wall can become the floor.", big=True),
   img("space-race.png", "Space Race title screen with a rover and a dotted path to a planet"),
   items("What's in it", [("10 levels", "Play them in order or pick one from the level select."),
                          ("Rotation", "Hit a trigger and the world turns around the player."),
                          ("Portals", "Step in one and come out somewhere else on the map.")]),
   text("Making it", "We wrote it in C# in Unity. I rebuilt it for WebGL in 2026 so it plays in the browser. The source is on GitHub."),
  ]),
]

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
    links = [("Work", "/work/"), ("CV", "/cv/"), ("Email", f"mailto:{EMAIL}")]
    lis = "".join(f'<li><a href="{h}"{" aria-current=page" if n == cur else ""}>{n}</a></li>' for n, h in links)
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
    go = "Play and read more" if p["type"] == "games" else "Read walkthrough"
    return f"""<a class="card feature {color} reveal {cls}" href="/work/{p['slug']}/" data-type="{p['type']}">
  <span class="meta">{i:02d} · {label}</span>
  <h3>{p['title']}</h3>
  <p>{p['tag']}</p>
  <div><div class="stat">{n}</div><p>{cap}</p></div>
  {tags(p['stack'][:4])}
  <span class="go">{go}</span>
</a>"""

def section(s):
    kind = s[0]
    if kind == "text":
        _, label, html, big = s
        body = f'<p class="lede prose">{html}</p>' if big else f'<div class="prose muted">{html if html.startswith("<") else "<p>" + html + "</p>"}</div>'
        return f'<section class="sec grid g-side reveal"><p class="eyebrow">{label}</p>{body}</section>'
    if kind == "steps":
        _, label, xs = s
        cells = "".join(f'<div class="step reveal"><span class="n">0{j+1}</span><b>{t}</b><p>{d}</p></div>' for j, (t, d) in enumerate(xs))
        return f'<section class="sec"><p class="eyebrow reveal">{label}</p><div class="grid g{len(xs)}">{cells}</div></section>'
    if kind == "nums":
        _, label, xs = s
        return f'<section class="sec reveal"><p class="eyebrow">{label}</p><div class="nums">' + "".join(f"<div><b>{n}</b><span>{c}</span></div>" for n, c in xs) + "</div></section>"
    if kind == "table":
        _, label, hd, rows, note = s
        th = "".join(f'<th scope="col">{h}</th>' for h in hd)
        trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        n = f'<p class="muted prose" style="margin-top:20px">{note}</p>' if note else ""
        return f'<section class="sec grid g-side reveal"><p class="eyebrow">{label}</p><div><div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>{n}</div></section>'
    if kind == "items":
        _, label, xs = s
        lis = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in xs)
        return f'<section class="sec grid g-side reveal"><p class="eyebrow">{label}</p><ul class="defs">{lis}</ul></section>'
    if kind == "img":
        _, src, alt = s
        return f'<section class="sec reveal"><img class="shot" src="/img/{src}" alt="{alt}" loading="lazy"></section>'
    raise ValueError(kind)

def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w") as f: f.write(html)

# Home. Staggered layout.
sel = [p for p in P if p["slug"] in ("mcp-verify", "bizbrief")]
home = head("Zachary Kaplan", "Zachary Kaplan is a backend developer interested in using data to make business decisions.") + nav("") + f"""
<section class="hero stair">
  <div style="grid-column:1/-1" class="reveal">
    <p class="eyebrow short">Backend developer</p>
    <h1 class="name"><span>Zachary</span><span>Kaplan</span></h1>
  </div>
  <div class="hero-bio reveal">
    <p class="lede">I'm most interested in using data to make business decisions.</p>
    <p class="muted" style="margin-top:1em">I graduated from Pomona with a degree in Computer Science and a minor in Economics. Right now I work on the backend at Umee Social. The problems I care about most involve user engagement, revenue and marketing.</p>
  </div>
  <div class="hero-now reveal">
    <p class="eyebrow">Now</p>
    <p><b>Backend developer</b> at <a href="https://www.umee.social">Umee Social</a></p>
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

<section class="sec stair">
  <div class="about reveal">
    <p class="eyebrow">About</p>
    <p class="lede">I want to work where engineering and analytics meet.</p>
    <div class="muted" style="margin-top:1em">
      <p>That could be backend, data or product work. The questions I like most are about why users stay, what they pay for and which marketing works.</p>
      <p>I'm looking for a team with experienced people I can learn from. I want to take on more responsibility as I grow.</p>
      <p>Outside of work I coach water polo at The Hill School. I also build things on the side, like a <a href="/work/water-polo-playbook/">playbook app</a> for the team and a couple of <a href="/work/?type=games">Unity games</a>.</p>
    </div>
  </div>
  <div class="edu reveal">
    <p class="eyebrow">Education</p>
    <h2>Pomona<br>College</h2>
    <p class="muted" style="margin-top:.8em">B.A. Computer Science. Minor in Economics.</p>
    <ul class="facts" style="margin-top:24px">
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
work = head("Work · Zachary Kaplan", "Projects by Zachary Kaplan. AI systems, data research, apps and games.") + nav("Work") + f"""
<section class="hero reveal">
  <p class="eyebrow short">{len(P)} projects</p>
  <h1 class="page">Work</h1>
  <p class="lede muted prose" style="margin-top:.5em">Everything here is finished and linked. Pick a type or open a card for the details.</p>
</section>
<div class="filters" role="group" aria-label="Filter projects by type">{chips}</div>
<section class="grid g2" aria-label="Projects">
{chr(10).join(card(p, i + 1) for i, p in enumerate(P))}
</section>
""" + foot()
write("work/index.html", work)

# Walkthroughs. Sections differ per project.
for i, p in enumerate(P):
    label, color = TYPES[p["type"]]
    prev_p, next_p = P[i - 1], P[(i + 1) % len(P)]
    links = "".join(f'<a class="btn" href="{h}">{n} ↗</a>' for n, h in p["links"])
    page = head(f"{p['title'].replace('&amp;', '&')} · Zachary Kaplan", p["claim"]) + nav("Work") + f"""
<section class="hero reveal">
  <p class="eyebrow short">{label} · {p['year']}</p>
  <h1 class="page">{p['title']}</h1>
  <p class="lede prose" style="margin-top:.6em">{p['claim']}</p>
  <div class="links">{links}</div>
</section>
{chr(10).join(section(s) for s in p['sections'])}
<section class="sec grid g-side reveal"><p class="eyebrow">Built with</p><div>{tags(p['stack'], 'quiet-tags')}</div></section>
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

cv = head("CV · Zachary Kaplan", "CV for Zachary Kaplan, backend developer.") + nav("CV") + f"""
<section class="hero reveal">
  <p class="eyebrow short">Curriculum vitae</p>
  <h1 class="page">Zachary Kaplan</h1>
  <p class="lede muted" style="margin-top:.6em">Backend developer. Interested in work that mixes engineering and analytics.</p>
  <div class="links no-print"><a class="btn" href="/Zachary_Kaplan-Resume.pdf" download>Download PDF ↓</a><a class="btn alt" href="mailto:{EMAIL}">Email ↗</a><a class="btn alt" href="{LI}">LinkedIn ↗</a></div>
</section>
<section class="sec grid g-side reveal"><p class="eyebrow">Experience</p><div>
{role("Umee Social", "https://www.umee.social", "Backend Developer", "Oct 2026 to now", [
  "Improve the admin panel and community health board on the backend.",
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

# ponytail: self-check. Every internal link resolves, no private repo link, no dashes in copy.
for f in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True):
    src = open(f).read()
    for href in re.findall(r'href="(/[^"#?]*)', src):
        target = os.path.join(OUT, href.lstrip("/"))
        assert os.path.exists(target if not href.endswith("/") else target + "index.html"), (f, href)
    assert "water-polo-playbook-pomona" not in src, f
    assert not re.search("[–—]", src), (f, "em or en dash in copy")
print("built", len(glob.glob(os.path.join(OUT, '**/*.html'), recursive=True)), "pages, checks OK")
