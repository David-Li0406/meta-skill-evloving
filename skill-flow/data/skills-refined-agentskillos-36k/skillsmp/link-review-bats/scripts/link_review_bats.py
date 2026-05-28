#!/usr/bin/env python3
"""
Interactive helper to link unassociated bat ids to review summary files.
Scans data/bats.yaml and data/reviews/summaries/*.yaml, suggests matches,
and updates associated_bat_ids after confirmation.
"""

import argparse
import glob
import os
import re
import sys
from difflib import SequenceMatcher

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Missing dependency: pyyaml")
    print("Install with: python3 -m pip install pyyaml")
    sys.exit(1)


def normalize_text(value):
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


BRAND_ALIASES = {
    "slugger": "louisvilleslugger",
    "louisville": "louisvilleslugger",
    "louisvilleslugger": "louisvilleslugger",
}


def normalize_brand(value):
    norm = normalize_text(value)
    if not norm:
        return ""
    return BRAND_ALIASES.get(norm, norm)


def normalize_sport(value):
    if value is None:
        return ""
    norm = normalize_text(value)
    if "fastpitch" in norm:
        return "fastpitch"
    if "slowpitch" in norm:
        return "slowpitch"
    if "baseball" in norm:
        return "baseball"
    return norm


def sport_from_league(league):
    if league is None:
        return ""
    norm = normalize_text(league)
    if "fastpitch" in norm:
        return "fastpitch"
    if "slowpitch" in norm:
        return "slowpitch"
    if norm:
        return "baseball"
    return ""

def tokenize_model(value):
    if value is None:
        return []
    tokens = re.split(r"[^a-z0-9]+", str(value).lower())
    return [token for token in tokens if token]


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_associated_ids(value):
    if value is None:
        return []
    if isinstance(value, int):
        return [value]
    text = str(value).strip()
    if not text:
        return []
    if (text.startswith("'") and text.endswith("'")) or (
        text.startswith('"') and text.endswith('"')
    ):
        text = text[1:-1]
    ids = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return ids


def parse_bat_type(value):
    tokens = set(tokenize_model(value))
    if not tokens:
        return None, None
    piece = None
    if "hybrid" in tokens:
        piece = "hybrid"
    elif "two" in tokens or "2" in tokens:
        piece = "two"
    elif "one" in tokens or "single" in tokens:
        piece = "single"
    material = None
    if "alloy" in tokens:
        material = "alloy"
    if "composite" in tokens:
        material = "composite"
    return piece, material


def bat_type_score(bat_type, review_type):
    bat_piece, bat_material = parse_bat_type(bat_type)
    review_piece, review_material = parse_bat_type(review_type)
    score = 0.0
    if bat_piece and review_piece:
        if bat_piece == review_piece:
            score += 0.6
        else:
            score -= 0.6
    if bat_material and review_material:
        if bat_material == review_material:
            score += 0.3
        else:
            score -= 0.3
    return score


def model_token_score(bat_tokens, review_tokens):
    if not bat_tokens or not review_tokens:
        return 0.0
    bat_set = set(bat_tokens)
    review_set = set(review_tokens)
    overlap = bat_set & review_set
    if not overlap:
        return 0.0
    coverage_review = len(overlap) / len(review_set)
    coverage_bat = len(overlap) / len(bat_set)
    score = coverage_review * 3.0 + coverage_bat * 1.5
    if coverage_review == 1.0:
        score += min(len(review_set), 4) * 0.25
    return score


def load_bats(bats_path):
    with open(bats_path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if isinstance(data, dict) and isinstance(data.get("bats"), dict):
        data = data.get("bats")
    bats = []
    items = []
    if isinstance(data, dict):
        items = list(data.items())
    elif isinstance(data, list):
        items = list(enumerate(data))
    for key, bat in items:
        if not isinstance(bat, dict):
            continue
        bat_id = parse_int(key) or parse_int(bat.get("id"))
        if bat_id is None:
            continue
        brand = bat.get("brand")
        model = bat.get("model")
        bat_type = bat.get("type") or bat.get("bat_type")
        model_tokens = tokenize_model(model)
        model_norm = normalize_text(model)
        bats.append(
            {
                "id": bat_id,
                "year": bat.get("year"),
                "brand": brand,
                "brand_norm": normalize_brand(brand),
                "model": model,
                "model_tokens": model_tokens,
                "model_norm": model_norm,
                "league": bat.get("league"),
                "drop": bat.get("drop"),
                "bat_type": bat_type,
                "sport_norm": sport_from_league(bat.get("league")),
            }
        )
    return bats


def load_reviews(review_dir):
    reviews = []
    associated_ids = set()
    for path in sorted(glob.glob(os.path.join(review_dir, "*.yaml"))):
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        review = data.get("review") or data
        if not isinstance(review, dict):
            review = {}
        associated = review.get("associated_bat_ids")
        ids = parse_associated_ids(associated)
        associated_ids.update(ids)
        brand = review.get("brand")
        model = review.get("model")
        reviews.append(
            {
                "path": path,
                "slug": review.get("slug")
                or data.get("slug")
                or os.path.basename(path),
                "year": review.get("year"),
                "brand": brand,
                "model": model,
                "sport": review.get("sport"),
                "bat_type": review.get("bat_type"),
                "associated_ids": ids,
                "norm_brand": normalize_brand(brand),
                "norm_model": normalize_text(model),
                "model_tokens": tokenize_model(model),
                "sport_norm": normalize_sport(review.get("sport")),
            }
        )
    return reviews, associated_ids


def sport_matches(league, sport):
    league_sport = sport_from_league(league)
    review_sport = normalize_sport(sport)
    if not league_sport or not review_sport:
        return None
    return league_sport == review_sport


def score_candidate(bat, review):
    score = 0.0
    bat_brand = bat.get("brand_norm") or normalize_brand(bat.get("brand"))
    review_brand = review.get("norm_brand", "")
    if bat_brand and review_brand:
        if bat_brand == review_brand:
            score += 3.0
        elif bat_brand in review_brand or review_brand in bat_brand:
            score += 1.5
    bat_model = bat.get("model_norm") or normalize_text(bat.get("model"))
    review_model = review.get("norm_model", "")
    if bat_model and review_model:
        ratio = SequenceMatcher(None, bat_model, review_model).ratio()
        score += ratio * 2.5
        if bat_model == review_model:
            score += 1.0
        elif bat_model in review_model or review_model in bat_model:
            score += 0.75
        score += model_token_score(bat.get("model_tokens"), review.get("model_tokens"))
    bat_year = parse_int(bat.get("year"))
    review_year = parse_int(review.get("year"))
    if bat_year and review_year:
        if bat_year == review_year:
            score += 1.5
        elif abs(bat_year - review_year) == 1:
            score += 0.75
    sport_match = sport_matches(bat.get("league"), review.get("sport"))
    if sport_match is True:
        score += 1.0
    elif sport_match is False:
        score -= 0.5
    score += bat_type_score(bat.get("bat_type"), review.get("bat_type"))
    return score


def suggest_reviews(bat, reviews, review_index, top_n, min_score):
    bat_brand = bat.get("brand_norm") or normalize_brand(bat.get("brand"))
    bat_year = parse_int(bat.get("year"))
    bat_sport = bat.get("sport_norm") or sport_from_league(bat.get("league"))
    candidates_pool = []
    if bat_brand and bat_year is not None:
        candidates_pool = review_index.get((bat_brand, bat_year), [])
    if bat_sport:
        candidates_pool = [
            review
            for review in candidates_pool
            if review.get("sport_norm") == bat_sport
        ]
    scored = []
    for review in candidates_pool:
        if not review.get("brand") or not review.get("model"):
            continue
        score = score_candidate(bat, review)
        scored.append((score, review))
    scored.sort(key=lambda item: item[0], reverse=True)
    strong = [item for item in scored if item[0] >= min_score][:top_n]
    if strong:
        return strong, True
    return scored[:top_n], False


def review_label(review):
    year = review.get("year") or "?"
    brand = review.get("brand") or "?"
    model = review.get("model") or "?"
    slug = review.get("slug") or os.path.basename(review.get("path", ""))
    return f"{slug} | {year} {brand} {model}"


def search_reviews(query, reviews):
    query_norm = normalize_text(query)
    hits = []
    for review in reviews:
        if not query_norm:
            continue
        if query_norm in normalize_text(review.get("slug")):
            hits.append(review)
            continue
        if query_norm in normalize_text(review.get("brand")):
            hits.append(review)
            continue
        if query_norm in normalize_text(review.get("model")):
            hits.append(review)
    return hits


def should_auto_select(scored, min_score, gap):
    if not scored:
        return False
    top_score = scored[0][0]
    if top_score < min_score:
        return False
    if len(scored) == 1:
        return True
    return (top_score - scored[1][0]) >= gap


def update_associated_ids(path, bat_id, dry_run=False):
    with open(path, "r", encoding="utf-8") as handle:
        lines = handle.readlines()
    pattern = re.compile(r"^(\s*associated_bat_ids:\s*)(.*)$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        prefix = match.group(1)
        raw_value = match.group(2).rstrip("\n")
        trimmed = raw_value.strip()
        quote = ""
        if (trimmed.startswith("'") and trimmed.endswith("'")) or (
            trimmed.startswith('"') and trimmed.endswith('"')
        ):
            quote = trimmed[0]
            trimmed = trimmed[1:-1]
        delimiter = ", "
        if "," in raw_value:
            delimiter = ", " if ", " in raw_value else ","
        existing_ids = []
        for part in trimmed.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                existing_ids.append(int(part))
            except ValueError:
                continue
        if bat_id in existing_ids:
            return False, raw_value.strip(), raw_value.strip()
        new_ids = existing_ids + [bat_id]
        new_value = delimiter.join(str(item) for item in new_ids)
        if quote:
            new_value = f"{quote}{new_value}{quote}"
        lines[index] = prefix + new_value + ("\n" if line.endswith("\n") else "")
        if not dry_run:
            with open(path, "w", encoding="utf-8") as handle:
                handle.writelines(lines)
        return True, raw_value.strip(), new_value
    raise RuntimeError("associated_bat_ids not found in review file")


def bat_matches_filters(bat, year, brand, model):
    if year and parse_int(bat.get("year")) != year:
        return False
    if brand and normalize_brand(bat.get("brand")) != normalize_brand(brand):
        return False
    if model and normalize_text(bat.get("model")) != normalize_text(model):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Find bats without review associations and link them interactively."
        )
    )
    parser.add_argument(
        "--repo",
        default="~/Coding_Projects/batdigest-flask",
        help="Path to batdigest-flask repo",
    )
    parser.add_argument("--year", type=int, help="Only process bats from this year")
    parser.add_argument("--brand", help="Only process bats from this brand")
    parser.add_argument("--model", help="Only process bats from this model")
    parser.add_argument("--limit", type=int, help="Maximum number of bats to process")
    parser.add_argument(
        "--top", type=int, default=5, help="Number of suggestions to show"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=2.5,
        help="Minimum score to consider a suggestion strong",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically apply high-confidence matches without prompting",
    )
    parser.add_argument(
        "--auto-gap",
        type=float,
        default=0.5,
        help="Minimum score gap between top and runner-up for auto mode",
    )
    parser.add_argument(
        "--auto-min-score",
        type=float,
        default=None,
        help="Override min-score threshold for auto mode",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without writing files"
    )
    args = parser.parse_args()

    repo = os.path.expanduser(args.repo)
    bats_path = os.path.join(repo, "data", "bats.yaml")
    reviews_dir = os.path.join(repo, "data", "reviews", "summaries")

    if not os.path.exists(bats_path):
        print(f"Missing bats file: {bats_path}")
        return 1
    if not os.path.isdir(reviews_dir):
        print(f"Missing review summaries: {reviews_dir}")
        return 1

    bats = load_bats(bats_path)
    reviews, associated_ids = load_reviews(reviews_dir)
    review_index = {}
    for review in reviews:
        key = review.get("norm_brand")
        year = parse_int(review.get("year"))
        if not key or year is None:
            continue
        review_index.setdefault((key, year), []).append(review)

    if not sys.stdin.isatty() and not args.auto:
        print("Non-interactive stdin detected. Use --auto to apply suggestions.")
        return 1

    unlinked = [
        bat
        for bat in bats
        if bat["id"] not in associated_ids
        and bat_matches_filters(bat, args.year, args.brand, args.model)
    ]

    if not unlinked:
        print("No unlinked bats found with current filters.")
        return 0

    unlinked.sort(key=lambda item: (-(parse_int(item.get("year")) or 0), item["id"]))

    processed = 0
    added = 0
    skipped = 0
    for bat in unlinked:
        if args.limit and processed >= args.limit:
            break
        processed += 1
        print("")
        print(
            f"Bat {bat['id']}: {bat.get('year')} {bat.get('brand')} "
            f"{bat.get('model')} {bat.get('league')} {bat.get('drop')}"
        )

        candidates, strong = suggest_reviews(
            bat, reviews, review_index, args.top, args.min_score
        )
        if candidates:
            banner = "Suggested reviews"
            if not strong:
                banner += " (low confidence)"
            print(banner + ":")
            for idx, (score, review) in enumerate(candidates, 1):
                print(f"  {idx}) {review_label(review)} [score {score:.2f}]")
        else:
            print("No review candidates found with metadata.")
            skipped += 1
            continue

        if args.auto:
            auto_min = args.auto_min_score if args.auto_min_score is not None else args.min_score
            if should_auto_select(candidates, auto_min, args.auto_gap):
                review = candidates[0][1]
                try:
                    updated, old_value, new_value = update_associated_ids(
                        review["path"], bat["id"], dry_run=args.dry_run
                    )
                except RuntimeError as exc:
                    print(str(exc))
                    skipped += 1
                    continue
                if updated:
                    added += 1
                    associated_ids.add(bat["id"])
                    review["associated_ids"].append(bat["id"])
                    print(
                        f"Updated {review.get('slug')} (associated_bat_ids: "
                        f"{old_value} -> {new_value})"
                    )
                else:
                    print(
                        f"Bat {bat['id']} already linked in {review.get('slug')}."
                    )
                    skipped += 1
                continue
            skipped += 1
            continue

        while True:
            choice = input(
                "Select review (1-{}), s=skip, q=quit, or type search text: ".format(
                    len(candidates)
                )
            ).strip()
            if not choice:
                continue
            if choice.lower() == "s":
                skipped += 1
                break
            if choice.lower() == "q":
                print("Stopping.")
                print(f"Processed: {processed}, added: {added}, skipped: {skipped}")
                return 0
            if choice.isdigit() and 1 <= int(choice) <= len(candidates):
                review = candidates[int(choice) - 1][1]
            else:
                matches = search_reviews(choice, reviews)
                if not matches:
                    print("No matches for search text.")
                    continue
                print("Search matches:")
                for idx, review in enumerate(matches[: args.top], 1):
                    print(f"  {idx}) {review_label(review)}")
                sub = input(
                    "Pick 1-{}, b=back, s=skip: ".format(
                        min(len(matches), args.top)
                    )
                ).strip()
                if sub.lower() == "b":
                    continue
                if sub.lower() == "s":
                    skipped += 1
                    break
                if not sub.isdigit() or not (1 <= int(sub) <= min(len(matches), args.top)):
                    print("Invalid selection.")
                    continue
                review = matches[int(sub) - 1]

            confirm = input(
                f"Add bat {bat['id']} to review {review.get('slug')}? [y/N]: "
            ).strip()
            if confirm.lower() != "y":
                skipped += 1
                break
            try:
                updated, old_value, new_value = update_associated_ids(
                    review["path"], bat["id"], dry_run=args.dry_run
                )
            except RuntimeError as exc:
                print(str(exc))
                skipped += 1
                break
            if updated:
                added += 1
                associated_ids.add(bat["id"])
                review["associated_ids"].append(bat["id"])
                print(
                    f"Updated {review.get('slug')} (associated_bat_ids: "
                    f"{old_value} -> {new_value})"
                )
            else:
                print(
                    f"Bat {bat['id']} already linked in {review.get('slug')}."
                )
                skipped += 1
            break

    print("")
    print(f"Processed: {processed}, added: {added}, skipped: {skipped}")
    if args.dry_run:
        print("Dry run enabled: no files were written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
