import importlib.util
import pathlib
import unittest
from unittest.mock import patch

path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "ebay_browse.py"
spec = importlib.util.spec_from_file_location("ebay_browse", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class EbayAdapterTest(unittest.TestCase):
    def test_market_codes(self):
        self.assertEqual(mod.MARKETS["ES"],"EBAY_ES")
        self.assertNotIn("PT", mod.MARKETS)

    def test_normalize_valid_listing(self):
        listing={
            "title":"Auriculares XYZ modelo 2",
            "seller":{"username":"Tienda ejemplo"},
            "price":{"value":"39.95","currency":"EUR"},
            "itemWebUrl":"https://www.ebay.es/itm/123",
            "shippingOptions":[{"shippingCost":{"value":"4.99","currency":"EUR"}}],
        }
        output=mod.normalize(listing,"ES","2026-11-21T12:00:00Z")
        self.assertEqual(output["price"],39.95)
        self.assertEqual(output["shipping"],4.99)
        self.assertFalse(output["affiliate"])

    def test_unknown_shipping(self):
        listing={"title":"Producto","price":{"value":"10","currency":"EUR"},
                 "itemWebUrl":"https://www.ebay.es/itm/123"}
        self.assertIsNone(mod.normalize(listing,"ES","2026-11-21T12:00:00Z")["shipping"])

    def test_reject_non_eur(self):
        listing={"title":"Product","price":{"value":"10","currency":"USD"},
                 "itemWebUrl":"https://www.ebay.com/itm/123"}
        self.assertIsNone(mod.normalize(listing,"ES","2026-11-21T12:00:00Z"))

    def test_affiliate_url_only_when_ebay_returns_it(self):
        listing={"title":"Product","price":{"value":"10","currency":"EUR"},
                 "itemWebUrl":"https://www.ebay.es/itm/123",
                 "itemAffiliateWebUrl":"https://www.ebay.es/itm/123?campid=example"}
        result=mod.normalize(listing,"ES","2026-11-21T12:00:00Z")
        self.assertTrue(result["affiliate"])
        self.assertIn("campid",result["url"])

    @patch.dict("os.environ",{},clear=True)
    def test_requires_secrets(self):
        with self.assertRaises(RuntimeError):
            mod.access_token()

if __name__=="__main__":
    unittest.main()
