import requests
import flet as ft
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


def parse_cookie_string(cookie_string):
    cookies = {}
    if not cookie_string:
        return cookies
    cookie_string = cookie_string.strip()
    # Accept both semicolon and newline as delimiters, robustly
    import re
    # Split on semicolon or newline, ignore empty parts
    pairs = re.split(r';|\n', cookie_string)
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        if '=' in pair:
            k, v = pair.split('=', 1)
            cookies[k.strip()] = v.strip()
    return cookies


def get_common_headers():
    return {
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


def get_csrf_token(cookies):
    import re
    csrf_cookie = cookies.get('_dnamatches-matchlistui-x-csrf-token')
    if csrf_cookie:
        return re.split(r'%7C|\|', csrf_cookie)[0]
    return None


VERSION = "0.1.5-alpha"


def main(page: ft.Page):
    page.title = f"MatchScope v{VERSION}"
    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False
    # Set app icon if supported
    try:
        page.window_icon = "icon.ico"
    except Exception:
        pass

    # Preload cookie.txt content if available
    try:
        with open("cookie.txt", "r", encoding="utf-8") as f:
            cookie_txt_content = f.read().strip()
    except Exception:
        cookie_txt_content = ""
    text_area = ft.TextField(
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=800,
        label="🍪 Paste your AncestryDNA browser cookie here",
        value=cookie_txt_content,
        visible=True,
        read_only=False
    )
    # Column of Rows, each Row holds up to 5 Cards (horizontal layout, 5 per row)
    output_cards_grid = ft.Column([], width=900, spacing=10)

    # Text widget for processing status below progress bar
    processing_status_text = ft.Text(value="", size=16, selectable=False)
    test_dropdown = ft.Dropdown(
        label="Select DNA Test", options=[], visible=False, width=400)
    # Radio buttons for match type
    # Store match counts for each type
    match_type_counts = {"all": None, "close": None, "distant": None}

    def get_match_type_label(mt):
        base = {
            "all": "All matches",
            "close": "Close matches (4th cousin or closer)",
            "distant": "Distant matches"
        }[mt]
        count = match_type_counts.get(mt)
        return f"{base} ({count if count is not None else '...'})"
    match_type_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="all", label=get_match_type_label("all")),
            ft.Radio(value="close", label=get_match_type_label("close")),
            ft.Radio(value="distant", label=get_match_type_label("distant"))
        ]),
        value="all",
        visible=False
    )
    number_input = ft.TextField(
        label="Number",
        value="50",
        width=80,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    get_matches_btn = ft.ElevatedButton("Get Matches", visible=False)
    pause_btn = ft.ElevatedButton("Pause", visible=False)
    resume_btn = ft.ElevatedButton("Resume", visible=False)
    matches_thread = None  # Track the running thread
    import threading
    pause_event = threading.Event()
    resume_event = threading.Event()
    run_id = 0  # Incremented each time Get Matches is clicked
    # Remove match_count_text, use only match_count_number
    progress_bar = ft.ProgressBar(value=0.0, width=400, visible=False)

    tests_data = {}

    # Create a single SnackBar instance and add it to the page
    snack_bar = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack_bar
    page.overlay.append(snack_bar)

    def show_message(msg):
        snack_bar.content.value = msg
        snack_bar.open = True
        page.update()

    def clear_clicked(e):
        text_area.value = ""
        output_cards_grid.controls.clear()
        processing_status_text.value = ""
        test_dropdown.options = []
        test_dropdown.visible = False
        # removed match_count_number
        number_input.value = "50"
        number_input.visible = False
        page.update()

    def authenticate_clicked(e):
        cookie_string = text_area.value.strip()
        if not cookie_string:
            show_message("Please enter cookies.")
            return
        cookies = parse_cookie_string(cookie_string)
        headers = get_common_headers()
        url = "https://www.ancestry.com/api/navheaderdata/v1/header/data/user"
        try:
            resp = requests.get(url, headers=headers, cookies=cookies)
            if resp.status_code == 200:
                auth_json = resp.json()
                name = auth_json.get('user', {}).get('name')
                if name:
                    # Fetch tests
                    fetch_tests(headers, cookies)
                    test_dropdown.visible = True
                    text_area.visible = False
                    auth_btn.visible = False
                    clear_btn.visible = False
                    show_message(f"Authenticated as {name}")
                else:
                    show_message("Authentication failed.")
            else:
                show_message("Authentication failed.")
        except Exception as ex:
            show_message(f"Error: {ex}")
        number_input.visible = False
        page.update()

    def fetch_tests(headers, cookies):
        url = 'https://www.ancestry.com/dna/insights/api/dnaSubnav/tests'
        test_headers = headers.copy()
        test_headers['accept'] = 'application/json'
        test_headers['content-type'] = 'application/json'
        test_headers.pop('referer', None)
        try:
            resp = requests.get(url, headers=test_headers, cookies=cookies)
            tests_json = resp.json()
            nonlocal tests_data
            tests_data = {(t.get('testGuid') or t.get('subjectName'))
                           : t for t in tests_json.get('dnaSamplesData', [])}
            test_dropdown.options = [ft.dropdown.Option(key=k, text=t.get(
                'subjectName') or k) for k, t in tests_data.items()]
        except Exception as ex:
            test_dropdown.options = []
            show_message(f"Failed to fetch tests: {ex}")
        page.update()

    def dropdown_changed(e):
        selected = test_dropdown.value
        if not selected or selected not in tests_data:
            # removed match_count_number and match_count_label
            get_matches_btn.visible = False
            number_input.visible = False
            page.update()
            return
        get_matches_btn.visible = True
        number_input.visible = True
        match_type_radio.visible = True
        fetch_and_show_match_count()
        page.update()

    def fetch_and_show_match_count():
        selected = test_dropdown.value
        if not selected or selected not in tests_data:
            # removed match_count_number and match_count_label
            return
        test_guid = selected
        url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchCount/{test_guid}"
        cookie_string = text_area.value.strip()
        cookies = parse_cookie_string(cookie_string)
        headers = get_common_headers()
        headers['referer'] = f"https://www.ancestry.com/discoveryui-matches/"
        headers['content-type'] = 'application/json'
        csrf_token = get_csrf_token(cookies)
        if csrf_token:
            headers['x-csrf-token'] = csrf_token
        # Fetch all 3 match type counts in sequence, update radio labels

        def fetch_count_for_type(mt):
            if mt == "close":
                payload = {"lower": 0, "upper": 9}
            elif mt == "distant":
                payload = {"lower": 10, "upper": 10}
            else:
                payload = {"lower": 0, "upper": 10}
            try:
                resp = requests.post(
                    url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("count")
            except Exception:
                pass
            return None
        for mt in ["all", "close", "distant"]:
            match_type_counts[mt] = fetch_count_for_type(mt)
        # Update radio labels
        match_type_radio.content.controls[0].label = get_match_type_label(
            "all")
        match_type_radio.content.controls[1].label = get_match_type_label(
            "close")
        match_type_radio.content.controls[2].label = get_match_type_label(
            "distant")
        # Show count for selected type
        match_type = match_type_radio.value if hasattr(
            match_type_radio, 'value') else "all"
        count = match_type_counts.get(match_type)
        # removed match_count_number and match_count_label
        page.update()

    import threading
    import queue

    def get_matches_clicked(e):
        nonlocal matches_thread, run_id
        run_id += 1
        this_run = run_id
        progress_bar.visible = False
        output_cards_grid.controls.clear()
        processing_status_text.value = ""
        pause_btn.visible = False  # Only show after we start fetching
        resume_btn.visible = False
        pause_event.clear()
        resume_event.set()
        page.update()

        def process_matches_thread():
            # Only update UI if this_run == run_id
            selected = test_dropdown.value
            if not selected or selected not in tests_data:
                if this_run == run_id:
                    show_message("Please select a valid DNA test.")
                    page.update()
                return
            test_guid = selected
            cookie_string = text_area.value.strip()
            cookies = parse_cookie_string(cookie_string)
            headers = get_common_headers()
            headers['referer'] = f"https://www.ancestry.com/discoveryui-matches/"
            headers['content-type'] = 'application/json'
            csrf_token = get_csrf_token(cookies)
            if csrf_token:
                headers['x-csrf-token'] = csrf_token
            count_url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchCount/{test_guid}"
            # Determine payload based on match type
            match_type = match_type_radio.value if hasattr(
                match_type_radio, 'value') else "all"
            if match_type == "close":
                payload = {"lower": 0, "upper": 9}
            elif match_type == "distant":
                payload = {"lower": 10, "upper": 10}
            else:
                payload = {"lower": 0, "upper": 10}
            try:
                resp = requests.post(
                    count_url, headers=headers, cookies=cookies, json=payload, allow_redirects=False)
                if resp.status_code == 200:
                    data = resp.json()
                    match_count = data.get("count", 0)
                    if not match_count:
                        if this_run == run_id:
                            show_message("No matches found.")
                            page.update()
                        return
                    total_pages = (match_count + 99) // 100
                else:
                    if this_run == run_id:
                        show_message(
                            "Failed to fetch match count for matches.")
                        page.update()
                    return
            except Exception as ex:
                if this_run == run_id:
                    show_message(f"Error fetching match count: {ex}")
                    page.update()
                return
            import sys
            try:
                max_matches = int(number_input.value)
            except Exception:
                max_matches = 50
            printed = 0
            import time
            import csv
            all_region_labels = set()
            matches_data = []
            import datetime
            today_str = datetime.datetime.now().strftime("%Y%m%d")
            csv_filename = f"matches_{test_guid}_{today_str}.csv"
            match_list_accum = []
            # Step 1: Fetch matches (as before, but accumulate for next step)
            # Calculate how many pages are actually needed for the requested max_matches
            needed_pages = (max_matches + 99) // 100
            # Show pause/resume buttons now that we're starting fetching
            if this_run == run_id:
                pause_btn.visible = True
                resume_btn.visible = False
                page.update()
            for page_num in range(1, min(total_pages, needed_pages) + 1):
                if printed >= max_matches:
                    break
                # Pause/Resume logic for page fetching
                while pause_event.is_set():
                    resume_btn.visible = True
                    pause_btn.visible = False
                    page.update()
                    resume_event.wait()
                resume_btn.visible = False
                pause_btn.visible = True
                # Progress bar for page fetching
                progress_bar.visible = True
                progress_bar.value = page_num / needed_pages
                # Show processing label for each page fetch (page fetching phase)
                processing_status_text.value = f"Fetching page {page_num}/{needed_pages}..."
                page.update()
                # Build URL based on match type
                if match_type == "distant":
                    url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={page_num}&sharedDna=distantMatches"
                elif match_type == "close":
                    url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={page_num}&sharedDna=closeMatches"
                else:
                    url = f"https://www.ancestry.com/discoveryui-matches/parents/list/api/matchList/{test_guid}?itemsPerPage=100&currentPage={page_num}"
                try:
                    resp = requests.get(url, headers=headers, cookies=cookies)
                    if resp.status_code == 200:
                        matches_json = resp.json()
                        match_list = matches_json.get("matchList", [])
                        for match in match_list:
                            if printed >= max_matches:
                                break
                            profile = match.get("matchProfile", {})
                            display_name = profile.get("displayName", "?")
                            sample_id = match.get("sampleId", "?")
                            shared_cm = match.get("relationship", {}).get(
                                "sharedCentimorgans", "")
                            match_list_accum.append({
                                "display_name": display_name,
                                "sample_id": sample_id,
                                "sharedCM": shared_cm
                            })
                            print(f"{printed+1}. {display_name} | {sample_id}")
                            sys.stdout.flush()
                            printed += 1
                    else:
                        print(f"Failed to fetch matches for page {page_num}")
                        sys.stdout.flush()
                except Exception as ex:
                    print(f"Error fetching matches for page {page_num}: {ex}")
                    sys.stdout.flush()
                if printed < max_matches and page_num < min(total_pages, needed_pages):
                    time.sleep(2.5)
            # After all pages fetched, clear the processing label for match processing
            processing_status_text.value = ""
            page.update()
            # Step 2: For each match, fetch ethnicity and save to CSV

            def append_to_csv_smart(match_data, all_region_labels, filename, is_first_match=False):
                current_regions = sorted(all_region_labels)
                header = ["Display Name", "Sample ID",
                          "sharedCM"] + current_regions
                import os
                if is_first_match or not os.path.exists(filename):
                    with open(filename, "w", newline='', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        row = [match_data.get("display_name", ""), match_data.get(
                            "sample_id", ""), match_data.get("sharedCM", "")]
                        region_percents = match_data.get("regions", {})
                        for label in current_regions:
                            row.append(region_percents.get(label, ""))
                        writer.writerow(row)
                else:
                    existing_header = []
                    existing_data = []
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            existing_header = next(reader, [])
                            for row in reader:
                                if row:
                                    existing_data.append(row)
                    except Exception as e:
                        print(f"Error reading existing CSV: {e}")
                        existing_header = []
                        existing_data = []
                    existing_regions = set(existing_header[3:]) if len(
                        existing_header) > 3 else set()
                    new_regions = set(current_regions) - existing_regions
                    if new_regions:
                        print(
                            f"Rewriting CSV with {len(new_regions)} new columns: {sorted(new_regions)}")
                        with open(filename, "w", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(header)
                            for row in existing_data:
                                if len(row) >= 3:
                                    new_row = row[:3]
                                    old_regions = existing_header[3:] if len(
                                        existing_header) > 3 else []
                                    old_region_data = row[3:] if len(
                                        row) > 3 else []
                                    old_data_map = {}
                                    for i, region in enumerate(old_regions):
                                        if i < len(old_region_data):
                                            old_data_map[region] = old_region_data[i]
                                    for region in current_regions:
                                        new_row.append(
                                            old_data_map.get(region, ""))
                                    writer.writerow(new_row)
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", "")]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)
                    else:
                        with open(filename, "a", newline='', encoding="utf-8") as f:
                            writer = csv.writer(f)
                            row = [match_data.get("display_name", ""), match_data.get(
                                "sample_id", ""), match_data.get("sharedCM", "")]
                            region_percents = match_data.get("regions", {})
                            for label in current_regions:
                                row.append(region_percents.get(label, ""))
                            writer.writerow(row)
            for i, match in enumerate(match_list_accum):
                if this_run != run_id:
                    return
                # Pause/Resume logic
                while pause_event.is_set():
                    resume_btn.visible = True
                    pause_btn.visible = False
                    page.update()
                    resume_event.wait()
                resume_btn.visible = False
                pause_btn.visible = True
                page.update()
                display_name = match["display_name"]
                sample_id = match["sample_id"]
                shared_cm = match["sharedCM"]
                progress_str = f"[{i+1}/{len(match_list_accum)}]"

                progress_bar.visible = True
                progress_bar.value = (i+1)/len(match_list_accum)
                processing_status_text.value = f"Processing {i+1}/{len(match_list_accum)}: ({sample_id})..."
                page.update()
                url = f'https://www.ancestry.com/discoveryui-matchesservice/api/compare/{test_guid}/with/{sample_id}/ethnicity'
                region_dict = {}
                region_line = ""
                try:
                    resp = requests.get(url, headers=headers, cookies=cookies)
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
                                        label = REGION_LABELS.get(
                                            str(rid), str(rid))
                                        print(
                                            f"{progress_str} [COMPARE][rightList] resourceId: {rid} ({label}), percent: {pct}")
                                        if label and pct is not None:
                                            region_list.append((label, pct))
                            for label, pct in region_list:
                                if label not in region_dict or pct > region_dict[label]:
                                    region_dict[label] = pct
                            all_region_labels.update(region_dict.keys())
                            # Build region summary string for output
                            if region_dict:
                                region_line = ", ".join(f"{lbl}: {pct}%" for lbl, pct in sorted(
                                    region_dict.items(), key=lambda x: -x[1]))
                            else:
                                region_line = "No ethnicity data"
                    except Exception:
                        print(
                            f"{progress_str} [COMPARE] JSON for {sample_id}: <not JSON>")
                        region_line = "Error parsing ethnicity data"
                except Exception as e:
                    print(
                        f"{progress_str} [COMPARE] Error for {sample_id}: {e}")
                    region_line = f"Error fetching ethnicity: {e}"
                # Output: Bar chart for regions (sorted by percent descending)
                output_cards_grid.controls.clear()
                if region_dict:
                    sorted_regions = sorted(
                        region_dict.items(), key=lambda x: -x[1])
                    bars = []
                    max_label_len = max((len(lbl)
                                        for lbl, _ in sorted_regions), default=10)
                    bar_max_width = 500  # px, for 100%
                    for idx, (lbl, pct) in enumerate(sorted_regions, 1):
                        bar_width = int(bar_max_width * (pct / 100.0))
                        bars.append(
                            ft.Row([
                                ft.Text(lbl, size=16, width=180,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Container(
                                    content=ft.Container(
                                        bgcolor="#1976d2",
                                        border_radius=6,
                                        width=bar_width,
                                        height=28,
                                        alignment=ft.alignment.center_left,
                                        padding=ft.padding.only(left=8),
                                        content=ft.Text(
                                            f"{pct}%", size=15, color="#FFFFFF", weight=ft.FontWeight.BOLD)
                                    ),
                                    bgcolor="#e3e3e3",
                                    border_radius=6,
                                    width=bar_max_width,
                                    height=28,
                                    alignment=ft.alignment.center_left,
                                    margin=ft.margin.only(bottom=6)
                                )
                            ], alignment="start", spacing=12)
                        )
                    output_cards_grid.controls.extend(bars)
                else:
                    output_cards_grid.controls.append(
                        ft.Row([
                            ft.Text("No ethnicity data", size=16)
                        ], alignment="start")
                    )
                page.update()
                match_data = {
                    "display_name": display_name,
                    "sample_id": sample_id,
                    "sharedCM": shared_cm,
                    "regions": region_dict.copy()
                }
                matches_data.append(match_data)
                try:
                    append_to_csv_smart(
                        match_data, all_region_labels, csv_filename, is_first_match=(i == 0))
                    print(f"{progress_str} Saved to CSV: {csv_filename}")
                except Exception as e:
                    print(f"{progress_str} Error saving to CSV: {e}")
                time.sleep(2.5)

            if this_run == run_id:
                progress_bar.value = 1.0
                pause_btn.visible = False
                resume_btn.visible = False
                processing_status_text.value = "Processing done."
                show_message(
                    f"Done. {len(matches_data)} matches processed. Saved to {csv_filename}.")
                page.update()
        # Start the thread and track it
        matches_thread = threading.Thread(target=process_matches_thread)
        matches_thread.start()

    clear_btn = ft.ElevatedButton("Clear", on_click=clear_clicked)
    auth_btn = ft.ElevatedButton("Authenticate", on_click=authenticate_clicked)
    test_dropdown.on_change = dropdown_changed
    get_matches_btn.on_click = get_matches_clicked

    def pause_clicked(e):
        pause_event.set()
        resume_event.clear()
        pause_btn.visible = False
        resume_btn.visible = True
        page.update()

    def resume_clicked(e):
        pause_event.clear()
        resume_event.set()
        pause_btn.visible = True
        resume_btn.visible = False
        page.update()

    pause_btn.on_click = pause_clicked
    resume_btn.on_click = resume_clicked

    # Wrap all UI elements in a scrollable Column inside an Expanded Container so the whole app and output area can scroll if content overflows
    # Place match_count_text and "Matches" label to the left of number_input

    # Remove match count label and number from UI
    main_column = ft.Column([
        text_area,
        ft.Row([auth_btn, clear_btn]),
        test_dropdown,
        match_type_radio,
        ft.Row([
            number_input,
            get_matches_btn
        ], alignment="start", spacing=10),
        progress_bar,
        processing_status_text,
        ft.Row([pause_btn, resume_btn], alignment="start", spacing=10),
        output_cards_grid
    ], scroll="auto", expand=True)
    page.add(ft.Container(content=main_column, expand=True))


ft.app(target=main)
