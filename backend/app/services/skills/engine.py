import csv
import re
from math import log
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

SKILLS_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "skills" / "ui-ux-pro-max"
MAX_RESULTS = 5

CSV_CONFIG = {
    "style": {"file": "styles.csv", "search_cols": ["Style Category", "Keywords", "Best For", "Type", "AI Prompt Keywords"], "output_cols": ["Style Category", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Performance", "Accessibility", "Framework Compatibility", "Complexity", "AI Prompt Keywords", "CSS/Technical Keywords", "Implementation Checklist", "Design System Variables"]},
    "color": {"file": "colors.csv", "search_cols": ["Product Type", "Notes"], "output_cols": ["Product Type", "Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Background (Hex)", "Text (Hex)", "Notes"]},
    "chart": {"file": "charts.csv", "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Accessibility Notes"], "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "Color Guidance", "Accessibility Notes", "Library Recommendation", "Interactive Level"]},
    "landing": {"file": "landing.csv", "search_cols": ["Pattern Name", "Keywords", "Conversion Optimization", "Section Order"], "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]},
    "product": {"file": "products.csv", "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"], "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus"]},
    "ux": {"file": "ux-guidelines.csv", "search_cols": ["Category", "Issue", "Description", "Platform"], "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]},
    "typography": {"file": "typography.csv", "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"], "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"]},
    "icons": {"file": "icons.csv", "search_cols": ["Category", "Icon Name", "Keywords", "Best For"], "output_cols": ["Category", "Icon Name", "Keywords", "Library", "Import Code", "Usage", "Best For", "Style"]},
    "react": {"file": "react-performance.csv", "search_cols": ["Category", "Issue", "Keywords", "Description"], "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]},
    "web": {"file": "web-interface.csv", "search_cols": ["Category", "Issue", "Keywords", "Description"], "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]},
    "reasoning": {"file": "ui-reasoning.csv", "search_cols": ["Industry", "Rule", "Scenario"], "output_cols": ["Industry", "Rule", "Scenario", "Do", "Don't", "Rationale"]},
}

STACK_CONFIG = {
    "html-tailwind": "stacks/html-tailwind.csv",
    "react": "stacks/react.csv",
    "nextjs": "stacks/nextjs.csv",
    "astro": "stacks/astro.csv",
    "vue": "stacks/vue.csv",
    "nuxtjs": "stacks/nuxtjs.csv",
    "svelte": "stacks/svelte.csv",
    "flutter": "stacks/flutter.csv",
    "react-native": "stacks/react-native.csv",
    "shadcn": "stacks/shadcn.csv",
}

DOMAIN_KEYWORDS = {
    "color": ["color", "palette", "hex", "#", "rgb"],
    "chart": ["chart", "graph", "visualization", "trend", "bar", "pie", "scatter", "heatmap", "funnel"],
    "landing": ["landing", "page", "cta", "conversion", "hero", "testimonial", "pricing", "section"],
    "product": ["saas", "ecommerce", "fintech", "healthcare", "gaming", "portfolio", "crypto", "dashboard"],
    "style": ["style", "design", "ui", "minimalism", "glassmorphism", "dark mode", "flat", "tailwind"],
    "ux": ["ux", "usability", "accessibility", "wcag", "touch", "scroll", "animation", "navigation", "mobile"],
    "typography": ["font", "typography", "heading", "serif", "sans"],
    "icons": ["icon", "icons", "lucide", "heroicons", "symbol", "glyph"],
    "react": ["react", "next.js", "nextjs", "suspense", "memo", "rerender", "bundle", "rsc"],
    "web": ["aria", "focus", "outline", "semantic", "virtualize", "autocomplete", "form"],
}


class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0

    def tokenize(self, text):
        text = re.sub(r'[^\w\s]', ' ', str(text).lower())
        return [w for w in text.split() if len(w) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N
        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            score = 0
            doc_len = self.doc_lengths[idx]
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += idf * numerator / denominator
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)


def _load_csv(filepath: Path) -> List[dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def _search_csv(filepath: Path, search_cols: List[str], output_cols: List[str], query: str, max_results: int) -> List[dict]:
    if not filepath.exists():
        return []
    data = _load_csv(filepath)
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in data]
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)
    results = []
    for idx, score in ranked[:max_results]:
        if score > 0:
            row = data[idx]
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    return results


def detect_domain(query: str) -> str:
    query_lower = query.lower()
    scores = {domain: sum(1 for kw in keywords if kw in query_lower) for domain, keywords in DOMAIN_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "style"


def search(query: str, domain: Optional[str] = None, max_results: int = MAX_RESULTS) -> dict:
    if domain is None:
        domain = detect_domain(query)
    config = CSV_CONFIG.get(domain, CSV_CONFIG["style"])
    filepath = SKILLS_DATA_DIR / config["file"]
    if not filepath.exists():
        return {"error": f"Data file not found: {filepath}", "domain": domain}
    results = _search_csv(filepath, config["search_cols"], config["output_cols"], query, max_results)
    return {"domain": domain, "query": query, "file": config["file"], "count": len(results), "results": results}


def search_stack(query: str, stack: str, max_results: int = MAX_RESULTS) -> dict:
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}", "available": list(STACK_CONFIG.keys())}
    filepath = SKILLS_DATA_DIR / STACK_CONFIG[stack]
    if not filepath.exists():
        return {"error": f"Stack file not found: {filepath}", "stack": stack}
    search_cols = ["Category", "Guideline", "Description", "Do", "Don't"]
    output_cols = ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL"]
    results = _search_csv(filepath, search_cols, output_cols, query, max_results)
    return {"domain": "stack", "stack": stack, "query": query, "file": STACK_CONFIG[stack], "count": len(results), "results": results}


def list_domains() -> List[str]:
    return list(CSV_CONFIG.keys())


def list_stacks() -> List[str]:
    return list(STACK_CONFIG.keys())
