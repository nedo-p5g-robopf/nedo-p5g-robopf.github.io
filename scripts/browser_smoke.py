#!/usr/bin/env python3
"""Exercise the rendered site's filters, navigation, responsive layout, and a11y."""
import argparse
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:4000")
    parser.add_argument("--browser", default=shutil.which("chromium"))
    parser.add_argument("--output", default="test-results")
    parser.add_argument("--axe", help="Path to axe-core's axe.min.js (optional)")
    args = parser.parse_args()
    base = args.url.rstrip("/")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.browser, headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("response", lambda response: errors.append(f"HTTP {response.status}: {response.url}") if response.status >= 400 else None)

        page.goto(base + "/", wait_until="networkidle")
        expect(page.locator("h1")).to_contain_text("ロボットSI")
        expect(page.locator(".research-card")).to_have_count(6)
        page.screenshot(path=str(output / "home-desktop.png"), full_page=True)
        page.screenshot(path=str(output / "home-desktop-viewport.png"))
        page.get_by_role("link", name="研究開発成果を探す", exact=True).first.click()
        expect(page.locator(".research-card:visible")).to_have_count(16)
        page.locator('[data-filter="design"]').click()
        expect(page.locator(".research-card:visible")).to_have_count(5)
        expect(page.locator("#result-count")).to_contain_text("5 件")
        assert "stage=design" in page.url
        page.reload()
        expect(page.locator('[data-filter="design"]')).to_have_attribute("aria-pressed", "true")
        expect(page.locator(".research-card:visible")).to_have_count(5)
        page.locator(".reset-filters").first.click()
        page.locator("#research-search").fill("ＲＯＳＢｕｉｌｄｅｒ")
        expect(page.locator(".research-card:visible")).to_have_count(1)
        expect(page.locator(".research-card:visible h3")).to_contain_text("ROSBuilder")
        page.locator("#research-search").fill("イーソル")
        expect(page.locator(".research-card:visible")).to_have_count(1)
        page.locator("#research-search").fill("存在しない成果物12345")
        expect(page.locator(".empty-state")).to_be_visible()
        expect(page.locator("#result-count")).to_contain_text("0 件")
        page.get_by_role("button", name="すべての成果を表示", exact=True).click()
        expect(page.locator(".research-card:visible")).to_have_count(16)
        expect(page.locator("#research-search")).to_be_focused()
        page.locator("#public-only").check()
        expect(page.locator(".research-card:visible")).to_have_count(2)
        page.locator(".research-card:visible").filter(has_text="mc_rtc").get_by_role("link").click()
        expect(page.get_by_role("link", name="ソースコードを見る")).to_have_attribute("href", "https://github.com/jrl-umi3218/mc_rtc")
        page.go_back()
        expect(page.locator("#public-only")).to_be_checked()
        expect(page.locator(".research-card:visible")).to_have_count(2)
        page.goto(base + "/research/?stage=invalid&q=%3Cscript%3E", wait_until="networkidle")
        expect(page.locator('[data-filter="all"]')).to_have_attribute("aria-pressed", "true")
        expect(page.locator(".empty-state")).to_be_visible()
        print("PASS: filters, counts, full-width search, institution search, empty state, reset, URL restoration, public resources")

        routes = ["/", "/project/", "/research/", "/research/mc-rtc/", "/research/rosbuilder/"]
        for width in [1440, 768, 390, 320]:
            page.set_viewport_size({"width": width, "height": 900})
            for route in routes:
                page.goto(base + route, wait_until="networkidle")
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"Overflow at {width}: {route}"
                if args.axe and width in [1440, 390]:
                    page.add_script_tag(path=args.axe)
                    audit = page.evaluate("async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa']}})")
                    violations = [{"id": v["id"], "nodes": [{"target": n["target"], "reason": n.get("failureSummary")} for n in v["nodes"]]} for v in audit["violations"]]
                    assert not violations, f"Accessibility failures at {width} {route}: {violations}"
        print("PASS: no horizontal overflow on 5 page types at 1440 / 768 / 390 / 320 px")
        if args.axe:
            print("PASS: axe WCAG 2 A/AA and 2.1 AA checks on 5 page types at desktop and mobile widths")

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(base + "/", wait_until="networkidle")
        expect(page.locator("#main-nav")).not_to_be_visible()
        menu = page.get_by_role("button", name="メニュー")
        menu.click()
        expect(page.locator("#main-nav")).to_be_visible()
        page.keyboard.press("Escape")
        expect(page.locator("#main-nav")).not_to_be_visible()
        expect(menu).to_be_focused()
        menu.click()
        page.locator("#main-nav").get_by_role("link", name="参画機関", exact=True).click()
        expect(page.locator("#members")).to_be_in_viewport()
        expect(page.locator("#consortium-aist .member")).to_have_count(12)
        expect(page.locator("#consortium-kawasaki .member")).to_have_count(7)
        expect(page.locator("#consortium-takenaka .member")).to_have_count(6)
        page.goto(base + "/", wait_until="networkidle")
        page.screenshot(path=str(output / "home-mobile.png"), full_page=True)
        page.screenshot(path=str(output / "home-mobile-viewport.png"))
        page.goto(base + "/research/", wait_until="networkidle")
        page.screenshot(path=str(output / "research-mobile-viewport.png"))
        print("PASS: mobile menu, Escape/focus behavior, member anchor navigation")

        no_js = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
        fallback = no_js.new_page()
        fallback.goto(base + "/research/", wait_until="networkidle")
        expect(fallback.locator(".research-card:visible")).to_have_count(16)
        expect(fallback.locator("#main-nav")).to_be_visible()
        expect(fallback.locator(".catalog-tools")).not_to_be_visible()
        fallback.locator(".research-card").first.get_by_role("link").click()
        expect(fallback.locator("h1")).to_contain_text("品質向上")
        print("PASS: navigation and all research pages remain usable without JavaScript")
        assert not errors, errors
        print("PASS: no browser JavaScript errors or failed HTTP responses")
        browser.close()


if __name__ == "__main__":
    main()
