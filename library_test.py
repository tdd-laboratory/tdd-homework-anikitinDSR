import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Prove that library can extract date
    def test_correct_data_extract(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, "2015-07-25")

    # Test that date is valid (the middle number in the date is greater than 12 and 
    # the final number in the date is greater than 31)
    def test_valid_date_limits(self):
        self.assert_extract("I was born on 2015-13-25.", library.dates_iso8601)
        self.assert_extract("I was born on 2015-07-32.", library.dates_iso8601)
        self.assert_extract("I was born on 2015-13-32.", library.dates_iso8601)

    # Prove that we can exctract date with 'str' as month
    def test_extract_date_with_str_month(self):
        self.assert_extract("I was born on 25 Jan 2015.", library.dates_month_str, "25 Jan 2015")

    def test_extract_date_with_time_milliseconds(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123.", library.dates_iso8601, "2018-06-22 18:22:19.123")

    def test_extract_date_with_time_seconds_only(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.", library.dates_iso8601, "2018-06-22 18:22:19")

    def test_extract_date_with_time_minutes_only(self):
        self.assert_extract("I was born on 2018-06-22 18:22.", library.dates_iso8601, "2018-06-22 18:22")

    def test_extract_date_with_time_and_t_as_delimeter(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123.", library.dates_iso8601, "2018-06-22T18:22:19.123")
	
    def test_extract_date_with_time_timezone_as_MDT(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123MDT.", library.dates_iso8601, "2018-06-22 18:22:19.123MDT")

    def test_extract_date_with_time_timezone_as_Z(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123Z.", library.dates_iso8601, "2018-06-22 18:22:19.123Z")

    def test_extract_date_with_time_timezone_as_offset(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123-0800.", library.dates_iso8601, "2018-06-22 18:22:19.123-0800")

    def test_extract_date_with_time_timezone_as_MDT_t_as_delimeter(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123MDT.", library.dates_iso8601, "2018-06-22T18:22:19.123MDT")

    def test_extract_date_with_time_timezone_as_Z_t_as_delimeter(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123Z.", library.dates_iso8601, "2018-06-22T18:22:19.123Z")

    def test_extract_date_with_time_timezone_as_offset_t_as_delimeter(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123-0800.", library.dates_iso8601, "2018-06-22T18:22:19.123-0800")

    def test_extract_date_with_str_month_and_comma_as_separator(self):
        self.assert_extract("I was born on 25 Jun, 2017", library.dates_month_str, "25 Jun, 2017")

    def test_integers_comma_separeted(self):
        self.assert_extract("Some text and 123,456,789", library.integers, '123', '456', '789')

if __name__ == '__main__':
    unittest.main()
