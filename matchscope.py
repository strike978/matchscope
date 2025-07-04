# --- Standard Library Imports ---
import re
import time
import os
import datetime
import csv
import threading
from urllib.parse import unquote

# --- Third-Party Imports ---
import requests

# --- Tkinter Imports ---
import tkinter as tk
from tkinter import ttk, scrolledtext


class DNAFetch:
    VERSION = "0.1.2-alpha"

    def validate_and_update_get_matches_button(self):
        """
        Check if both pages and items per page have valid numbers.
        Also ensure pages to retrieve doesn't exceed total pages available.
        Enable/disable the Get Matches button accordingly.
        """
        if not self.auth_ok:
            self.get_matches_btn.config(state='disabled')
            return

        try:
            pages = int(self.pages_var.get())
            items_per_page = int(self.items_per_page_var.get())
            total_pages = self._get_total_pages_from_label()

            # Both fields must have positive numbers
            if pages > 0 and items_per_page > 0:
                # If we know the total pages, ensure pages to retrieve doesn't exceed it
                if total_pages is not None and pages > total_pages:
                    self.get_matches_btn.config(state='disabled')
                else:
                    self.get_matches_btn.config(state='normal')
            else:
                self.get_matches_btn.config(state='disabled')
        except (ValueError, Exception):
            # If either field is not a valid number, disable the button
            self.get_matches_btn.config(state='disabled')

    def _get_total_pages_from_label(self):
        """Extract total pages number from the label text."""
        total_pages_text = self.total_pages_label.cget('text')
        if 'Total Pages:' in total_pages_text:
            total_pages_str = total_pages_text.replace(
                'Total Pages:', '').strip()
            if total_pages_str != '?' and total_pages_str.isdigit():
                return int(total_pages_str)
        return None

    def on_pages_var_change(self, event=None):
        # Only update UI, do not cancel or pause any running retrieval here.
        # This method is intentionally a no-op except for UI updates.

        # Validate pages doesn't exceed total pages
        try:
            pages = int(self.pages_var.get())
            total_pages = self._get_total_pages_from_label()
            if total_pages is not None and pages > total_pages:
                # Auto-correct to max available pages
                self.pages_var.set(str(total_pages))
        except (ValueError, Exception):
            pass

        self.validate_and_update_get_matches_button()

    def _validate_items_per_page(self, items_per_page_str):
        """Validate and normalize items per page value."""
        try:
            items_per_page = int(items_per_page_str)
            if items_per_page > 100:
                return 100
            elif items_per_page < 20:
                return 20
            return items_per_page
        except Exception:
            return 50

    def _prepare_match_headers(self):
        """Prepare headers for match API requests."""
        match_headers = dict(self.headers)
        match_headers['accept'] = 'application/json'
        match_headers['content-type'] = 'application/json'
        match_headers.pop('referer', None)
        csrf_cookie = self.cookies.get('_dnamatches-matchlistui-x-csrf-token')
        if csrf_cookie:
            token = re.split(r'%7C|\|', csrf_cookie)[0]
            match_headers['x-csrf-token'] = token
        return match_headers

    def append_to_csv_smart(self, match_data, all_region_labels, filename, is_first_match=False):
        """
        Smart CSV append that handles changing column structures by rewriting when needed.
        """

        current_regions = sorted(all_region_labels)
        header = ["Display Name", "Sample ID", "sharedCM"] + current_regions

        if is_first_match or not os.path.exists(filename):
            # Create new file with header
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)

                # Write the current match
                row = [match_data.get("display_name", ""),
                       match_data.get("sample_id", ""),
                       match_data.get("sharedCM", "")]
                region_percents = match_data.get("regions", {})
                for label in current_regions:
                    row.append(region_percents.get(label, ""))
                writer.writerow(row)
        else:
            # Check if we need to rewrite due to new columns
            existing_header = []
            existing_data = []

            try:
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    existing_header = next(reader, [])
                    for row in reader:
                        if row:  # Skip empty rows
                            existing_data.append(row)
            except Exception as e:
                print(f"Error reading existing CSV: {e}")
                existing_header = []
                existing_data = []

            # Only rewrite if we have NEW columns that aren't in existing header
            existing_regions = set(existing_header[3:]) if len(
                existing_header) > 3 else set()
            new_regions = set(current_regions) - existing_regions

            if new_regions:
                # Need to rewrite entire file with new structure
                print(
                    f"Rewriting CSV with {len(new_regions)} new columns: {sorted(new_regions)}")

                with open(filename, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)

                    # Rewrite existing data with new column structure
                    for row in existing_data:
                        if len(row) >= 3:  # Must have at least name, id, cm
                            # Keep first 3 columns (name, id, cm)
                            new_row = row[:3]

                            # Map old region data to new structure
                            old_regions = existing_header[3:] if len(
                                existing_header) > 3 else []
                            old_region_data = row[3:] if len(row) > 3 else []

                            # Create mapping of old region data
                            old_data_map = {}
                            for i, region in enumerate(old_regions):
                                if i < len(old_region_data):
                                    old_data_map[region] = old_region_data[i]

                            # Add region data in new order
                            for region in current_regions:
                                new_row.append(old_data_map.get(region, ""))

                            writer.writerow(new_row)

                    # Add the new match
                    row = [match_data.get("display_name", ""),
                           match_data.get("sample_id", ""),
                           match_data.get("sharedCM", "")]
                    region_percents = match_data.get("regions", {})
                    for label in current_regions:
                        row.append(region_percents.get(label, ""))
                    writer.writerow(row)
            else:
                # Simple append - column structure hasn't changed
                with open(filename, "a", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    row = [match_data.get("display_name", ""),
                           match_data.get("sample_id", ""),
                           match_data.get("sharedCM", "")]
                    region_percents = match_data.get("regions", {})
                    for label in current_regions:
                        row.append(region_percents.get(label, ""))
                    writer.writerow(row)

    def export_to_csv(self, matches_data, region_labels, filename=None):
        """
        Export the matches data to a CSV file. Each row contains display name, sample ID, shared cM, and region percentages.
        region_labels: list of all region names (columns).
        """

        if filename is None:
            # Use test guid and current date as filename
            guid = getattr(self, 'selected_test_guid', 'unknown')
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            filename = f"ancestry_matches_{guid}_{date_str}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["Display Name", "Sample ID", "sharedCM"] + region_labels
            writer.writerow(header)
            for match in matches_data:
                row = [match.get("display_name", ""),
                       match.get("sample_id", ""),
                       match.get("sharedCM", "")]
                # Fill in region percentages in the order of region_labels
                region_percents = match.get("regions", {})
                for label in region_labels:
                    pct = region_percents.get(label, "")
                    row.append(pct)
                writer.writerow(row)

    REGION_LABELS = {
        "04800": "New Zealand Maori",
        "02500": "Bengal",
        "00200": "Mali",
        "06700": "Baltics",
        "04400": "Aboriginal and/or Torres Strait Islander Peoples",
        "02900": "Mongolia & Upper Central Asia",
        "00600": "Nigerian Woodlands",
        "06300": "Ashkenazi Jews",
        "04000": "Northern & Central Philippines",
        "06301": "Sephardic Jews",
        "08200": "Wales",
        "02100": "Burusho",
        "03700": "Dai",
        "01400": "Northern Africa",
        "07900": "Spain",
        "05600": "Indigenous Haiti & Dominican Republic",
        "03300": "Northern China",
        "01800": "Cyprus",
        "07500": "Northern Italy",
        "05200": "Indigenous Americas— Yucatán Peninsula ",
        "07100": "Aegean Islands",
        "01000": "Nilotic Peoples",
        "00900": "Eastern Bantu Peoples",
        "00503": "Nigeria",
        "02401": "Southern India",
        "02002": "Northern Iraq & Northern Iran",
        "00100": "Senegal",
        "06601": "Iceland",
        "03850": "Maritime Southeast Asia",
        "00502": "North-Central Nigeria",
        "06600": "Norway",
        "02800": "Northern Asia",
        "00501": "Central Nigeria",
        "02403": "The Deccan & the Gulf of Mannar",
        "04700": "Hawaii",
        "02402": "Southwest India",
        "06200": "Indigenous Eastern South America",
        "04300": "Melanesia",
        "08101": "Cornwall",
        "02001": "Lower Central Asia",
        "02000": "Iran/Persia",
        "08100": "England & Northwestern Europe",
        "05900": "Indigenous Americas—Ecuador",
        "01300": "Khoisan, Aka & Mbuti Peoples",
        "05500": "Indigenous Cuba",
        "01700": "Levant",
        "07800": "Basque",
        "03600": "Southern China",
        "05100": "Indigenous Americas—Mexico ",
        "07400": "Southern Italy & the Eastern Mediterranean",
        "06950": "Eastern European Roma",
        "03200": "Southern Japanese Islands",
        "07000": "Greece & Albania",
        "00800": "Southern Bantu Peoples",
        "02302": "Gujarat",
        "02301": "Western Himalayas & the Hindu Kush",
        "00760": "Twa",
        "00403": "Central West Africa",
        "06501": "Denmark",
        "00402": "Yorubaland",
        "06900": "The Balkans",
        "04600": "Samoa",
        "02700": "Tibetan Peoples",
        "00401": "Benin & Togo",
        "02303": "Gulf of Khambhat",
        "08400": "Ireland",
        "06500": "Sweden",
        "04200": "Guam",
        "08000": "Portugal",
        "06100": "Indigenous Americas—Chile",
        "03350": "Western China",
        "00750": "Western Bantu Peoples",
        "03900": "Vietnam",
        "01200": "Somalia",
        "07700": "Germanic Europe",
        "05800": "Indigenous Americas—Colombia & Venezuela",
        "03500": "Central & Eastern China",
        "01600": "Arabian Peninsula",
        "07701": "The Netherlands",
        "07300": "Sardinia",
        "05400": "Indigenous Americas—Panama & Costa Rica",
        "03100": "Japan",
        "04150": "Central & Southern Philippines",
        "04151": "Luzon",
        "05000": "Indigenous Americas—North",
        "04152": "Western Visayas",
        "04900": "Indigenous Arctic",
        "00300": "Ivory Coast & Ghana",
        "02200": "Indo-Gangetic Plain",
        "00700": "Cameroon",
        "04500": "Tonga",
        "06801": "Russia",
        "06800": "Central & Eastern Europe",
        "02600": "Nepal & the Himalayan Foothills",
        "06400": "Finland",
        "08300": "Scotland",
        "06000": "Indigenous Americas—Bolivia & Peru",
        "01900": "Anatolia & the Caucasus",
        "03800": "Mainland Southeast Asia",
        "01100": "Ethiopia & Eritrea",
        "03400": "Southwestern China",
        "05700": "Indigenous Puerto Rico",
        "01500": "Egypt",
        "07600": "France",
        "03000": "Korea",
        "05300": "Indigenous Americas—Central",
        "07200": "Malta"
    }

    def ensure_output_box(self):
        """
        Ensure the output text box and status label are present and visible in the UI.
        This is called after login and before retrieval to guarantee output widgets are available.
        """
        frm = self.root.children[list(self.root.children)[0]]
        # Add or update status label (directly above the output box)
        if not hasattr(self, 'status_label'):
            self.status_label = ttk.Label(frm, text="")
        self.status_label.config(text="")
        self.status_label.grid(
            row=4, column=0, columnspan=6, sticky='w', pady=(0, 5))
        if not hasattr(self, 'output_text'):
            self.output_text = scrolledtext.ScrolledText(
                frm, width=80, height=12, font=('TkDefaultFont', 10), state='disabled', wrap='word')
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')
        self.output_text.grid(
            row=5, column=0, columnspan=6, pady=10, sticky='nsew')
        frm.rowconfigure(5, weight=0)  # Remove extra vertical stretch

    def __init__(self, root):
        self.root = root
        self.root.title(f'MatchScope – AncestryDNA Edition v{self.VERSION}')

        # Set custom icon (cross-platform)
        try:
            # Try PNG first (works on all platforms)
            icon = tk.PhotoImage(file='icon.png')
            self.root.iconphoto(False, icon)
        except Exception:
            try:
                # Fallback to GIF (also cross-platform)
                icon = tk.PhotoImage(file='icon.gif')
                self.root.iconphoto(False, icon)
            except Exception:
                # If no icon files found, continue without icon
                pass

        self.session = requests.Session()

        # Hardcoded working headers
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.8",
            "ancestry-context-ube": "eyJldmVudElkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwiY29ycmVsYXRlZFNjcmVlblZpZXdlZElkIjoiY2FkNzQ3ZTQtODY2ZS00YjMxLWFiMTQtMTEzOTA5MzUzODg3IiwiY29ycmVsYXRlZFNlc3Npb25JZCI6ImQ5ZWRiOGRiLTYzMTEtNGRhMS1iNjM0LTlkMmQxYWUwMzZmZiIsInNjcmVlbk5hbWVTdGFuZGFyZCI6IiIsInNjcmVlbk5hbWUiOiIiLCJ1c2VyQ29uc2VudCI6Im5lY2Vzc2FyeXxwcmVmZXJlbmNlfHBlcmZvcm1hbmNlfGFuYWx5dGljczFzdHxhbmFseXRpY3MzcmR8YWR2ZXJ0aXNpbmcxc3R8YXR0cmlidXRpb24zcmQiLCJ2ZW5kb3JzIjoiIiwidmVuZG9yQ29uZmlndXJhdGlvbnMiOiJ7fSJ9",
            "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE2OTA1NzAiLCJhcCI6IjMxMjUwMjkyMyIsImlkIjoiNTg2NjcwY2EzMWEwZDA2OCIsInRyIjoiYjNjMjQzZTU0YzA3OWViYTg0NzU1ODVkYTQxZTIyNjkiLCJ0aSI6MTc1MTM4NjY3MjQxNywidGsiOiIyNjExNzUwIn19",
            "priority": "u=1, i",
            "referer": "https://www.ancestry.com/",
            "sec-ch-ua": "",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "traceparent": "00-b3c243e54c079eba8475585da41e2269-586670ca31a0d068-01",
            "tracestate": "2611750@nr=0-1-1690570-312502923-586670ca31a0d068----1751386672417",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }

        # Hardcoded working cookies
        self.cookies = {}
        self.tests_data = []
        self.selected_test_guid = ''
        self.name = None
        self.auth_ok = False
        self.build_ui()
        # Preload cookie data from cookie.txt if available
        try:
            with open('cookie.txt', 'r', encoding='utf-8') as f:
                cookie_data = f.read().strip()
            if cookie_data:
                self.cookie_text.insert('1.0', cookie_data)
        except Exception:
            pass

    def build_ui(self):
        """
        Build the main UI for the application, including all widgets and event bindings.
        This method is called once during initialization.
        """
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Simple authentication info
        self.auth_info_label = ttk.Label(
            frm, text='🍪 Paste your Ancestry.com browser cookies below to authenticate:')
        self.auth_info_label.grid(row=0, column=0, columnspan=4, sticky='w')

        # Cookie input
        self.cookie_text = scrolledtext.ScrolledText(frm, width=100, height=6)
        self.cookie_text.grid(row=1, column=0, columnspan=4,
                              sticky='ew', pady=(10, 0))

        # Authentication and clear buttons
        self.auth_btn = ttk.Button(
            frm, text='Authenticate', command=self.authenticate)
        self.auth_btn.grid(row=2, column=0, sticky='w', pady=(10, 0))
        self.clear_btn = ttk.Button(
            frm, text='Clear', command=self.clear_cookies)
        self.clear_btn.grid(row=2, column=1, sticky='w', pady=(10, 0))
        self.auth_error_label = ttk.Label(frm, text='', foreground='red')
        self.auth_error_label.grid(row=4, column=0, columnspan=6, sticky='w')
        self.auth_error_label.grid_remove()
        self.logout_btn = ttk.Button(
            frm, text='Sign Out', command=self.clear_all, state='disabled')
        self.logout_btn.grid(row=2, column=6, sticky='e', pady=(10, 0))
        self.logout_btn.grid_remove()

        # Test selection (hidden until authenticated)
        self.test_label = ttk.Label(frm, text='Select a test:')
        self.test_label.grid(row=2, column=4, sticky='e',
                             padx=(20, 2), pady=(10, 0))
        self.tests_combo = ttk.Combobox(frm, state='readonly')
        self.tests_combo.grid(row=2, column=5, sticky='w', pady=(10, 0))
        self.tests_combo.bind('<<ComboboxSelected>>', self.on_test_select)
        self.test_label.grid_remove()
        self.tests_combo.grid_remove()

        # Group for items per page and pages to retrieve (hidden until authenticated)
        self.page_group = ttk.LabelFrame(
            frm, text='Match Retrieval Options', padding=(5, 2, 5, 2))
        self.page_group.grid(row=3, column=2, columnspan=6,
                             sticky='w', padx=(10, 0))
        self.page_group.grid_remove()

        # Total pages label and entry for pages to retrieve
        self.total_pages_label = ttk.Label(
            self.page_group, text='Total Pages: ?')
        self.total_pages_label.grid(row=0, column=0, sticky='e', padx=(0, 5))
        self.pages_label = ttk.Label(
            self.page_group, text='Number of Pages:')
        self.pages_label.grid(row=0, column=1, sticky='e', padx=(0, 2))
        self.pages_var = tk.StringVar(value='1')
        self.pages_entry = ttk.Entry(
            self.page_group, textvariable=self.pages_var, width=6)
        self.pages_entry.grid(row=0, column=2, sticky='w', padx=(0, 10))

        # Items per page label and entry
        self.items_per_page_label = ttk.Label(
            self.page_group, text='Matches per Page:')
        self.items_per_page_label.grid(
            row=0, column=3, sticky='e', padx=(0, 2))
        self.items_per_page_var = tk.StringVar(value='50')
        self.items_per_page_entry = ttk.Entry(
            self.page_group, textvariable=self.items_per_page_var, width=6)
        self.items_per_page_entry.grid(
            row=0, column=4, sticky='w', padx=(0, 10))

        # Get Matches button (hidden until authenticated)
        self.get_matches_btn = ttk.Button(
            self.page_group, text='Get Matches', command=self.get_matches, state='disabled')
        self.get_matches_btn.grid(row=0, column=5, sticky='w')
        self.get_matches_btn.grid_remove()

        # Leeds Method button (hidden until authenticated)
        # self.leeds_btn = ttk.Button(
        #     frm, text='Leeds Method', command=self.leeds_method)
        # self.leeds_btn.grid(row=4, column=2, sticky='w', padx=(10, 0))
        # self.leeds_btn.grid_remove()

        # Bind items per page change to update total pages label only
        self.items_per_page_entry.bind(
            '<FocusOut>', self.on_items_per_page_change)
        self.items_per_page_entry.bind(
            '<Return>', self.on_items_per_page_change)
        # Also bind to validate Get Matches button on input change
        self.items_per_page_var.trace(
            'w', lambda *args: self.validate_and_update_get_matches_button())

        # Bind pages to retrieve change to update UI only (do not cancel retrieval)
        self.pages_entry.bind('<FocusOut>', self.on_pages_var_change)
        self.pages_entry.bind('<Return>', self.on_pages_var_change)
        # Also bind to validate Get Matches button on input change
        self.pages_var.trace(
            'w', lambda *args: self.validate_and_update_get_matches_button())

        # Pause button (hidden until retrieval starts)
        self.pause_btn = ttk.Button(
            frm, text='Pause', command=self.toggle_pause, state='disabled')
        self.pause_btn.grid(row=5, column=2, columnspan=6,
                            sticky='w', pady=(8, 0))
        self.pause_btn.grid_remove()

        frm.rowconfigure(5, weight=1)

    def toggle_pause(self):
        if not hasattr(self, '_pause_event'):
            return
        if self._pause_event.is_set():
            # Currently running, so pause
            self._pause_event.clear()
            self.pause_btn.config(text='▶️ Resume')
        else:
            # Currently paused, so resume
            self._pause_event.set()
            self.pause_btn.config(text='⏸️ Pause')

    def _cancel_retrieval(self):
        """Cancel any running retrieval thread."""
        self._retrieval_cancelled = True
        if hasattr(self, '_retrieval_thread') and self._retrieval_thread is not None:
            if self._retrieval_thread.is_alive():
                try:
                    self._retrieval_thread.join(timeout=1)
                except Exception:
                    pass
            self._retrieval_thread = None
        # Reset the pause event so it is ready for next retrieval
        if hasattr(self, '_pause_event'):
            self._pause_event.set()

    def _clear_output_widgets(self):
        """Hide and clear output/status widgets."""
        if hasattr(self, 'output_text'):
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', tk.END)
            self.output_text.config(state='disabled')
            self.output_text.grid_remove()
        if hasattr(self, 'status_label'):
            self.status_label.config(text='')
            self.status_label.grid_remove()

    def clear_cookies(self):
        """Clear only the cookie text box."""
        self.cookie_text.delete('1.0', tk.END)
        self.auth_error_label.config(text='')
        self.auth_error_label.grid_remove()

    def clear_all(self):
        # Reset UI to initial state
        self.auth_info_label.grid(row=0, column=0, columnspan=4, sticky='w')
        self.cookie_text.grid(row=1, column=0, columnspan=4,
                              sticky='ew', pady=(10, 0))
        # Clear the cookie text when signing out
        self.cookie_text.delete('1.0', tk.END)
        self.auth_btn.config(state='normal')
        self.auth_btn.grid(row=2, column=0, sticky='w', pady=(10, 0))
        self.clear_btn.grid(row=2, column=1, sticky='w', pady=(10, 0))
        self.auth_error_label.config(text='')
        self.auth_error_label.grid_remove()
        self.tests_combo.grid_remove()
        self.test_label.grid_remove()
        self.get_matches_btn.grid_remove()
        # self.leeds_btn.grid_remove()
        self.logout_btn.config(state='disabled')
        self.logout_btn.grid_remove()
        self.pause_btn.config(state='disabled')
        self.pause_btn.grid_remove()
        self.page_group.grid_remove()

        # Reset application state
        self.name = None
        self.auth_ok = False
        self.tests_data = []
        self.selected_test_guid = ''
        self.cookies = {}  # Clear cookies on logout

        # Cancel any running retrieval thread
        self._cancel_retrieval()

        # Hide and clear output/status widgets
        self._clear_output_widgets()

    def print_output(self, text, clear=False):
        # Append text to the output_text area, or clear if clear=True
        if hasattr(self, 'output_text'):
            self.output_text.config(state='normal')
            if clear:
                self.output_text.delete('1.0', tk.END)
            # Insert at the top, not the end
            self.output_text.insert('1.0', text)
            self.output_text.config(state='disabled')

    def is_matches_endpoint(self, url):
        return url and '/discoveryui-matches/parents/list/api/matchList/' in url

    def parse_cookie_string(self, cookie_string):
        """Parse a browser cookie string into a dictionary."""
        cookies = {}
        if not cookie_string:
            return cookies

        # Handle both semicolon-separated and line-separated formats
        cookie_string = cookie_string.strip()

        # Split by semicolons or newlines
        if ';' in cookie_string:
            pairs = cookie_string.split(';')
        else:
            pairs = cookie_string.split('\n')

        for pair in pairs:
            pair = pair.strip()
            if '=' in pair:
                k, v = pair.split('=', 1)
                cookies[k.strip()] = v.strip()

        return cookies

    def authenticate(self):
        # Use hardcoded headers with user-provided cookies
        self.auth_error_label.config(text='')

        cookie_string = self.cookie_text.get('1.0', tk.END).strip()
        if not cookie_string:
            self.auth_error_label.config(
                text='Please paste your browser cookies.')
            self.auth_error_label.grid()
            return

        # Parse cookies from user input
        self.cookies = self.parse_cookie_string(cookie_string)

        url = 'https://www.ancestry.com/api/navheaderdata/v1/header/data/user'

        try:
            resp = self.session.get(
                url, headers=self.headers, cookies=self.cookies)

            if resp.status_code == 200:
                auth_json = resp.json()
                self.name = auth_json.get('user', {}).get('name')
                if self.name:
                    self.auth_ok = True
                    self.fetch_tests()
                    self.auth_btn.config(state='disabled')
                    self.auth_btn.grid_remove()
                    self.clear_btn.grid_remove()
                    self.cookie_text.grid_remove()
                    self.auth_info_label.grid_remove()
                    self.auth_error_label.grid_remove()
                    self.logout_btn.config(state='normal')
                    self.logout_btn.grid()  # Show log out button
                    # Start disabled until fields validated
                    self.get_matches_btn.config(state='disabled')
                    self.tests_combo.grid()
                    self.test_label.grid()
                    self.page_group.grid()  # Show grouped controls
                    self.get_matches_btn.grid()  # Show Get Matches button
                    # self.leeds_btn.grid()  # Show Leeds Method button
                    self.pause_btn.config(state='disabled')
                    self.pause_btn.grid_remove()
                    # Update total pages label after authentication
                    if self.tests_data and self.selected_test_guid:
                        self.update_total_pages_and_label(
                            self.selected_test_guid)
                else:
                    self.auth_error_label.config(
                        text='Authentication failed: No user name found.')
                    self.auth_error_label.grid()
            else:
                self.auth_error_label.config(
                    text=f'Authentication failed: Status {resp.status_code}')
                self.auth_error_label.grid()
        except Exception as e:
            self.auth_error_label.config(text=f'Authentication error: {e}')
            self.auth_error_label.grid()

    def on_items_per_page_change(self, event=None):
        # Called when items per page entry changes.
        # Only updates the total pages label; does NOT cancel or pause any running retrieval.
        if not self.auth_ok or not self.selected_test_guid:
            return

        items_per_page = self._validate_items_per_page(
            self.items_per_page_var.get())
        self.items_per_page_var.set(str(items_per_page))

        test_guid = self.selected_test_guid
        matches_url = f'https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage={items_per_page}&currentPage=1'
        match_headers = self._prepare_match_headers()

        try:
            resp = self.session.get(
                matches_url, headers=match_headers, cookies=self.cookies)
            match_json = resp.json()
            total_pages = match_json.get('totalPages', '?')
            self.total_pages_label.config(text=f"Total Pages: {total_pages}")
            self.validate_and_update_get_matches_button()
        except Exception:
            pass

    def fetch_tests(self):
        url = 'https://www.ancestry.com/dna/insights/api/dnaSubnav/tests'
        test_headers = self._prepare_match_headers()

        try:
            resp = self.session.get(
                url, headers=test_headers, cookies=self.cookies)
            tests_json = resp.json()
            self.tests_data = tests_json.get('dnaSamplesData', [])
            if self.tests_data:
                self.tests_combo['values'] = [
                    t.get('subjectName', t.get('testGuid', '')) for t in self.tests_data]
                self.tests_combo.current(0)
                self.selected_test_guid = self.tests_data[0].get(
                    'testGuid', '')
                self.update_total_pages_and_label(self.selected_test_guid)
                self.validate_and_update_get_matches_button()
        except Exception:
            pass

    def on_test_select(self, event):
        # Called when the user selects a different test from the dropdown.
        # Only updates the selected test and total pages label; does NOT cancel or pause any running retrieval.
        idx = self.tests_combo.current()
        if 0 <= idx < len(self.tests_data):
            self.selected_test_guid = self.tests_data[idx].get('testGuid', '')
            self.update_total_pages_and_label(self.selected_test_guid)
            # Update Get Matches button state after test selection
            self.validate_and_update_get_matches_button()

    def update_total_pages_and_label(self, test_guid):
        if not self.auth_ok or not test_guid:
            return

        items_per_page = self._validate_items_per_page(
            self.items_per_page_var.get())
        matches_url = f'https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage={items_per_page}&currentPage=1'
        match_headers = self._prepare_match_headers()

        try:
            resp = self.session.get(
                matches_url, headers=match_headers, cookies=self.cookies)
            match_json = resp.json()
            total_pages = match_json.get('totalPages', '?')
            self.total_pages_label.config(text=f"Total Pages: {total_pages}")
            self.validate_and_update_get_matches_button()
        except Exception:
            self.total_pages_label.config(text="Total Pages: ?")
            self.validate_and_update_get_matches_button()

    def _wait_with_pause_check(self, seconds):
        """Wait for the specified number of seconds while checking for pause and cancellation."""
        iterations = int(seconds * 10)  # Check every 0.1 seconds
        for _ in range(iterations):
            if getattr(self, '_retrieval_cancelled', False):
                return
            if not self._pause_event.is_set():
                while not self._pause_event.is_set():
                    if getattr(self, '_retrieval_cancelled', False):
                        return
                    time.sleep(0.1)
            time.sleep(0.1)

    def get_matches(self):
        # Start a new retrieval, cancelling any running retrieval first

        # Cancel any running retrieval before starting a new one
        self._retrieval_cancelled = True
        if hasattr(self, '_retrieval_thread') and self._retrieval_thread is not None:
            if self._retrieval_thread.is_alive():
                try:
                    self._retrieval_thread.join(timeout=1)
                except Exception:
                    pass
            self._retrieval_thread = None

        # Prevent multiple retrievals at once
        if hasattr(self, '_retrieval_thread') and self._retrieval_thread is not None and self._retrieval_thread.is_alive():
            self.status_label.config(
                text="A retrieval is already in progress. Please wait.")
            return

        # Reset retrieval cancelled flag
        self._retrieval_cancelled = False

        if not hasattr(self, '_pause_event'):
            self._pause_event = threading.Event()
            self._pause_event.set()

        def worker():
            # This thread performs the match retrieval and CSV export
            self.root.after(0, lambda: (self.pause_btn.config(
                state='normal', text='⏸️ Pause'), self.pause_btn.grid()))
            if not self.auth_ok or not self.selected_test_guid or getattr(self, '_retrieval_cancelled', False):
                self.root.after(0, lambda: (self.pause_btn.config(
                    state='disabled'), self.pause_btn.grid_remove()))
                return
            self.root.after(0, self.ensure_output_box)

            items_per_page = self._validate_items_per_page(
                self.items_per_page_var.get())
            try:
                num_pages = int(self.pages_var.get())
            except Exception:
                num_pages = 1

            all_sample_ids = set()
            all_matches = []
            # Reset pause event in case it was left cleared from a previous run
            if hasattr(self, '_pause_event'):
                self._pause_event.set()

            # First phase: collect all matches
            for page in range(num_pages):
                if getattr(self, '_retrieval_cancelled', False):
                    return
                page_num = page + 1

                def update_page_status(page=page, num_pages=num_pages):
                    self.status_label.config(
                        text=f"Retrieving matches: Page {page_num} of {num_pages}...")
                self.root.after(0, update_page_status)

                if page > 0:
                    self._wait_with_pause_check(2.5)  # 2.5 seconds delay
                    if getattr(self, '_retrieval_cancelled', False):
                        return

                matches_url = f'https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{self.selected_test_guid}?itemsPerPage={items_per_page}&currentPage={page_num}'
                print(f"Requesting page {page_num}: {matches_url}")
                match_headers = self._prepare_match_headers()

                try:
                    resp = self.session.get(
                        matches_url, headers=match_headers, cookies=self.cookies)
                    print(
                        f"Response status for page {page_num}: {resp.status_code}")
                    match_json = resp.json()
                    match_list = match_json.get('matchList', [])
                    print(
                        f"Page {page_num} returned {len(match_list)} matches.")
                    for m in match_list:
                        sample_id = m.get('sampleId', '')
                        if sample_id and sample_id not in all_sample_ids:
                            all_sample_ids.add(sample_id)
                            all_matches.append(m)
                except Exception as e:
                    print(
                        f'Error: Could not fetch matches on page {page_num}: {e}')
                    self.pause_btn.config(state='disabled')
                    return

            def clear_output():
                self.output_text.config(state='normal')
                self.output_text.delete('1.0', tk.END)
                self.output_text.config(state='disabled')
            self.root.after(0, clear_output)

            # Second phase: process matches and collect region data
            total_matches = len(all_matches)
            all_region_labels = set()
            matches_data = []

            # Initialize CSV file and filename

            guid = getattr(self, 'selected_test_guid', 'unknown')
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            csv_filename = f"ancestry_matches_{guid}_{date_str}.csv"

            for i, m in enumerate(all_matches):
                if getattr(self, '_retrieval_cancelled', False):
                    return
                sample_id = m.get('sampleId', '')
                prof = m.get('matchProfile', {})
                display_name = prof.get('displayName', '')
                shared_cm = m.get('relationship', {}).get(
                    'sharedCentimorgans', '')
                if not sample_id:
                    continue

                progress_str = f"[{i+1}/{total_matches}]"
                url = f'https://www.ancestry.com/discoveryui-matchesservice/api/compare/{self.selected_test_guid}/with/{sample_id}/ethnicity'

                def update_status(i=i, total_matches=total_matches, sample_id=sample_id, shared_cm=shared_cm):
                    cm_text = f" - {shared_cm} cM" if shared_cm else ""
                    self.status_label.config(
                        text=f"Processing {i+1}/{total_matches} (Sample ID: {sample_id}{cm_text})...")
                self.root.after(0, update_status)

                region_dict = {}
                try:
                    resp = self.session.get(
                        url, headers=self.headers, cookies=self.cookies)
                    print(
                        f"{progress_str} [COMPARE] Response for {sample_id}: {resp.status_code}")
                    try:
                        resp_json = resp.json()
                        if isinstance(resp_json, dict) and "comparisons" in resp_json:
                            region_list = []
                            for comp in resp_json["comparisons"]:
                                if "rightList" in comp:
                                    for entry in comp["rightList"]:
                                        rid = entry.get("resourceId")
                                        pct = entry.get("percent")
                                        label = self.REGION_LABELS.get(
                                            str(rid), "Unknown")
                                        print(
                                            f"{progress_str} [COMPARE][rightList] resourceId: {rid} ({label}), percent: {pct}")
                                        if label and pct is not None:
                                            region_list.append((label, pct))
                            for label, pct in region_list:
                                if label not in region_dict or pct > region_dict[label]:
                                    region_dict[label] = pct
                            all_region_labels.update(region_dict.keys())
                            sorted_regions = sorted(
                                region_dict.items(), key=lambda x: -x[1])

                            def insert_sorted_rightlist(sorted_regions=sorted_regions, sample_id=sample_id):
                                if not sorted_regions:
                                    out = "No regions found."
                                else:
                                    lines = [
                                        f"{i+1}. {pct}% {label}" for i, (label, pct) in enumerate(sorted_regions)]
                                    out = '\n'.join(lines)
                                self.print_output(out, clear=True)
                            self.root.after(0, insert_sorted_rightlist)
                    except Exception:
                        print(
                            f"{progress_str} [COMPARE] JSON for {sample_id}: <not JSON>")
                except Exception as e:
                    print(
                        f"{progress_str} [COMPARE] Error for {sample_id}: {e}")

                    def insert_error(sample_id=sample_id, e=e):
                        self.print_output(f"Error for {sample_id}: {e}")
                    self.root.after(0, insert_error)

                # Create match data for this single match
                match_data = {
                    "display_name": display_name,
                    "sample_id": sample_id,
                    "sharedCM": shared_cm,
                    "regions": region_dict.copy()
                }
                matches_data.append(match_data)

                # Save this match to CSV immediately (progressive saving)
                try:
                    # Use smart CSV method that handles changing column structures
                    self.append_to_csv_smart(
                        match_data, all_region_labels, csv_filename, is_first_match=(i == 0))
                    print(f"{progress_str} Saved to CSV: {csv_filename}")
                except Exception as e:
                    print(f"{progress_str} Error saving to CSV: {e}")

                if i < total_matches - 1:
                    self._wait_with_pause_check(2.5)  # 2.5 seconds delay
                    if getattr(self, '_retrieval_cancelled', False):
                        return

            def finish_status():
                self.status_label.config(
                    text=f"Done. All {total_matches} matches saved to {csv_filename}")
            self.root.after(0, finish_status)

            def finish_output():
                self.pause_btn.config(state='disabled', text='⏸️ Pause')
                self.pause_btn.grid_remove()
            self.root.after(0, finish_output)
            # Mark thread as finished
            self._retrieval_thread = None

        self._retrieval_thread = threading.Thread(target=worker, daemon=True)
        self._retrieval_thread.start()

    def leeds_method(self):
        """
        Retrieve all pages from the Leeds Method endpoint using the current test GUID.
        Print each page's response to the console with a 2.5s delay and a blank line between outputs.
        """
        import tkinter.messagebox as messagebox
        messagebox.showinfo(
            "Leeds Method", "The Leeds Method feature is not functional yet.")
        if not self.auth_ok or not self.selected_test_guid:
            print("Not authenticated or no test selected.")
            return
        guid = self.selected_test_guid
        base_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{guid}?sharedDna=90-400&currentPage={{}}"
        headers = self._prepare_match_headers()
        total_pages = 1
        all_matches = []
        # First, get page 1 to determine totalPages
        try:
            resp = self.session.get(base_url.format(
                1), headers=headers, cookies=self.cookies)
            print(
                f"Leeds Method response for GUID {guid} (page 1): {resp.status_code}")
            print(resp.text)
            try:
                data = resp.json()
                total_pages = int(data.get('totalPages', 1))
                match_list = data.get('matchList', [])
                all_matches.extend(match_list)
            except Exception:
                print("Could not parse totalPages from response; defaulting to 1 page.")
        except Exception as e:
            print(f"Leeds Method error (page 1): {e}")
            return
        # Fetch remaining pages if any
        for page in range(2, total_pages + 1):
            time.sleep(2.5)
            try:
                resp = self.session.get(base_url.format(
                    page), headers=headers, cookies=self.cookies)
                print("\n")  # Blank line between page outputs
                print(
                    f"Leeds Method response for GUID {guid} (page {page}): {resp.status_code}")
                print(resp.text)
                try:
                    data = resp.json()
                    match_list = data.get('matchList', [])
                    all_matches.extend(match_list)
                except Exception:
                    print(
                        f"Could not parse matchList from page {page} response.")
            except Exception as e:
                print(f"Leeds Method error (page {page}): {e}")
        # After all pages, extract displayName and sampleId, count and print
        name_id_list = []
        for m in all_matches:
            prof = m.get('matchProfile', {})
            display_name = prof.get('displayName', None)
            sample_id = m.get('sampleId', None)
            if display_name and sample_id:
                name_id_list.append((display_name, sample_id))
        print(f"\nTotal Leeds matches: {len(name_id_list)}")
        for i, (display_name, sample_id) in enumerate(name_id_list, 1):
            print(f"{i}. {display_name} | {sample_id}")


if __name__ == '__main__':
    root = tk.Tk()
    app = DNAFetch(root)
    root.mainloop()
