#!/usr/bin/env python3
"""Haki Digital social image renderer.

Usage:  python3 render.py spec.json out.png
Spec (JSON):
  type:    "blog" | "tip" | "result" | "quote"
  theme:   "light" | "dark"          (optional; blog defaults dark, others light)
  eyebrow: short label, e.g. "New on the Playbook"   (optional, has defaults)
  title:   main headline (blog, tip)                 or the quote text (quote)
  sub:     supporting line (optional)
  number:  big figure for result, e.g. "$591,194"
  label:   what the number is (result)
  name / role: quote attribution
  cta:     button text (optional; blog defaults "Read the guide")
Output: 1080x1350 PNG (4:5, Facebook/Instagram feed size).
Needs playwright + Chrome, and the fonts BricolageGrotesque-Bold/Regular.ttf and
InstrumentSans-Regular/Bold.ttf (looked for next to this script in fonts/, then
in /mnt/skills/examples/canvas-design/canvas-fonts/).
"""
import json, os, sys, html, pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT_DIRS = [HERE / "fonts", pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")]
CHROME = next((p for p in ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"] if os.path.exists(p)), None)


def font(name):
    for d in FONT_DIRS:
        f = d / name
        if f.exists():
            return f.as_uri()
    sys.exit(f"font not found: {name}")


HAT = ('<svg viewBox="4 10 112 45" class="{cls}"><defs><clipPath id="c{cls}"><path d="M26 43V36C26 20 41 10 60 10S94 20 94 36V43Z"/></clipPath></defs>'
       '<path d="M26 43V36C26 20 41 10 60 10S94 20 94 36V43Z" fill="#E8B858"/><g clip-path="url(#c{cls})" stroke="#C9952F" stroke-width="2.5"><path d="M20 24h80M20 31h80"/></g>'
       '<rect x="26" y="36" width="68" height="7" fill="{band}"/><rect x="4" y="46" width="112" height="9" rx="4.5" fill="#C9952F"/></svg>')


def build(s):
    t = s.get("type", "tip")
    dark = s.get("theme", "dark" if t == "blog" else "light") == "dark"
    e = lambda k, d="": html.escape(str(s.get(k, d)))
    eyebrow = e("eyebrow", {"blog": "New on the Playbook", "tip": "Marketing tip", "result": "Real results", "quote": "Client words"}[t])
    band = "#19211F" if not dark else "#FBF8F1"
    if t == "result":
        main = f'<div class="num">{e("number")}</div><div class="label">{e("label")}</div>' + (f'<p class="sub">{e("sub")}</p>' if s.get("sub") else "")
    elif t == "quote":
        main = (f'<div class="qmark">&ldquo;</div><blockquote class="fit">{e("title")}</blockquote>'
                f'<div class="who"><b>{e("name")}</b><span>{e("role")}</span></div>')
    else:
        main = f'<h1 class="fit">{e("title")}</h1>' + (f'<p class="sub">{e("sub")}</p>' if s.get("sub") else "")
    cta = e("cta", "Read the guide" if t == "blog" else "")
    foot_r = f'<span class="cta">{cta} &rarr;</span>' if cta else '<span class="loc">Ads · Email · Design · Automation</span>'
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:B;src:url({font('BricolageGrotesque-Bold.ttf')});font-weight:700}}
@font-face{{font-family:B;src:url({font('BricolageGrotesque-Regular.ttf')});font-weight:400}}
@font-face{{font-family:S;src:url({font('InstrumentSans-Regular.ttf')});font-weight:400}}
@font-face{{font-family:S;src:url({font('InstrumentSans-Bold.ttf')});font-weight:700}}
*{{margin:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{--bg:{'#19211F' if dark else '#FBF8F1'};--ink:{'#FBF8F1' if dark else '#19211F'};--mut:{'#C9C2B2' if dark else '#4A4F4C'};--acc:{'#E8B858' if dark else '#A8422D'};--line:{'#3A4440' if dark else '#DDD5C3'};
background:var(--bg);color:var(--ink);font-family:S;position:relative}}
.frame{{position:absolute;inset:72px 80px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:center;gap:18px;font:700 34px B;letter-spacing:-.01em}}
.brand svg{{width:84px}}
.brand small{{display:block;font:400 20px S;color:var(--mut);letter-spacing:.02em}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0;padding:40px 0}}
.eyebrow{{font:700 24px S;letter-spacing:.16em;text-transform:uppercase;color:var(--acc);margin-bottom:34px;display:flex;align-items:center;gap:16px}}
.eyebrow:before{{content:"";width:44px;height:3px;background:var(--acc)}}
h1{{font:700 104px/1.02 B;letter-spacing:-.03em;max-height:640px;overflow:hidden}}
.sub{{font:400 36px/1.4 S;color:var(--mut);margin-top:36px;max-width:880px}}
.num{{font:700 190px/1 B;letter-spacing:-.04em;color:var(--acc)}}
.label{{font:700 52px/1.15 B;letter-spacing:-.02em;margin-top:26px;max-width:880px}}
.qmark{{font:700 220px/.6 B;color:#E8B858;height:110px}}
blockquote{{font:400 56px/1.28 B;letter-spacing:-.015em;max-height:720px;overflow:hidden}}
.who{{margin-top:44px;font:400 28px/1.4 S;color:var(--mut)}}
.who b{{display:block;font:700 32px S;color:var(--ink)}}
.foot{{display:flex;justify-content:space-between;align-items:center;border-top:2px solid var(--line);padding-top:34px;font:400 26px S;color:var(--mut)}}
.cta{{background:{'#E8B858' if dark else '#A8422D'};color:{'#19211F' if dark else '#FBF8F1'};font:700 28px S;padding:20px 34px;border-radius:999px}}
.wm{{position:absolute;right:-70px;top:150px;width:460px;opacity:{'.10' if dark else '.0'}}}
</style></head><body>
{HAT.format(cls='wm', band=band) if dark else ''}
<div class="frame">
 <div class="brand">{HAT.format(cls='logo', band=band)}<div>Haki Digital<small>Marketing &amp; Automation</small></div></div>
 <div class="main"><div class="eyebrow">{eyebrow}</div>{main}</div>
 <div class="foot"><span>Spokane, WA</span>{foot_r}</div>
</div>
<script>
document.fonts.ready.then(()=>{{document.querySelectorAll('.fit').forEach(el=>{{
 let fs=parseFloat(getComputedStyle(el).fontSize);
 const mx=parseFloat(getComputedStyle(el).maxHeight);
 while(el.scrollHeight>mx&&fs>34){{fs-=2;el.style.fontSize=fs+'px'}}
}});document.body.dataset.ready=1}});
</script></body></html>"""


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    from playwright.sync_api import sync_playwright
    page_html = build(spec)
    tmp = pathlib.Path(out).resolve().with_suffix(".html")
    tmp.write_text(page_html)
    with sync_playwright() as p:
        b = p.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(tmp.as_uri())
        pg.wait_for_selector("body[data-ready]", timeout=15000)
        pg.screenshot(path=out)
        b.close()
    tmp.unlink()
    print("wrote", out)


if __name__ == "__main__":
    main()
