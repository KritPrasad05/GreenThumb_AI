import os, time, requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

V2_BASE = "https://api.eppo.int/gd/v2"
GD_BASE = "https://gd.eppo.int"   # public website, no auth needed


class EPPOClient:
    def __init__(self, timeout: int = 15, delay: float = 1.0):
        self.timeout = timeout
        self.delay = delay
        self.token = os.getenv("EPPO_API_TOKEN")
        if not self.token:
            raise RuntimeError("EPPO_API_TOKEN not set")
        self.headers = {"X-API-Key": self.token, "Accept": "application/json"}

    def _get_v2(self, endpoint: str, params: Dict = None):
        time.sleep(self.delay)
        r = requests.get(
            f"{V2_BASE}{endpoint}",
            headers=self.headers,
            params=params or {},
            timeout=self.timeout
        )
        if r.status_code == 200:
            return r.json()
        print(f"  [v2 WARN] {r.status_code} for {endpoint}")
        return None

    def _get_gd_page(self, path: str) -> Optional[str]:
        """Fetch raw HTML from the public EPPO GD website."""
        time.sleep(self.delay)
        r = requests.get(f"{GD_BASE}{path}", timeout=self.timeout)
        if r.status_code == 200:
            return r.text
        return None

    # ── v2 API calls ────────────────────────────────────────────────────────

    def name_to_codes(self, name: str) -> List[Dict]:
        result = self._get_v2("/tools/name2codes", {"name": name, "onlyPreferred": "false"})
        return result if isinstance(result, list) else []

    def get_taxon(self, eppo_code: str) -> Optional[Dict]:
        return self._get_v2(f"/taxon/{eppo_code}")

    def get_names(self, eppo_code: str) -> Optional[List]:
        return self._get_v2(f"/taxon/{eppo_code}/names")

    def get_hosts_v2(self, eppo_code: str) -> Optional[List]:
        return self._get_v2(f"/taxon/{eppo_code}/hosts")

    def get_categorization_v2(self, eppo_code: str) -> Optional[List]:
        return self._get_v2(f"/taxon/{eppo_code}/categorization")

    # ── GD website scraping (public, no auth) ───────────────────────────────

    def get_gd_hosts(self, eppo_code: str) -> List[str]:
        """
        Scrape host plant list from gd.eppo.int/taxon/{code}/hosts
        Returns list of host plant names.
        """
        from bs4 import BeautifulSoup
        html = self._get_gd_page(f"/taxon/{eppo_code}/hosts")
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        hosts = []
        for row in soup.select("table.table tbody tr"):
            cells = row.find_all("td")
            if cells:
                hosts.append(cells[0].get_text(strip=True))
        return hosts

    def get_gd_overview(self, eppo_code: str) -> str:
        """
        Scrape the overview/datasheet text from gd.eppo.int/taxon/{code}
        Returns raw text for embedding.
        """
        from bs4 import BeautifulSoup
        html = self._get_gd_page(f"/taxon/{eppo_code}")
        if not html:
            return ""
        soup = BeautifulSoup(html, "html.parser")
        # Remove nav/footer/script noise
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        main = soup.find("div", {"id": "main-content"}) or soup.find("main") or soup.body
        return main.get_text(separator=" ", strip=True)[:3000] if main else ""

    def get_full_profile(self, eppo_code: str) -> Dict:
        """Fetch everything and return unified dict."""
        profile = {"eppo_code": eppo_code}
        profile["taxon"]          = self.get_taxon(eppo_code)
        profile["names"]          = self.get_names(eppo_code)
        profile["hosts_api"]      = self.get_hosts_v2(eppo_code)
        profile["categorization"] = self.get_categorization_v2(eppo_code)
        profile["hosts_web"]      = self.get_gd_hosts(eppo_code)
        profile["overview_text"]  = self.get_gd_overview(eppo_code)
        return profile