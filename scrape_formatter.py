def scrape(parameters):

    # Create base url for all further searches
    base_url = create_url(parameters)

    # Output list and frame
    output = []

    for x in range(0, parameters["pages"]):
        if x == 0:
            page_append = ""
        else:
            page_append = "&start=" + str(x * 10)

        # get page
        current_page = requests.get(base_url + page_append, timeout=5)
        page_soup = BeautifulSoup(current_page.content, "html.parser")

        for job in page_soup.select(".jobsearch-SerpJobCard"):
            (
                title,
                company,
                url,
                description,
                rating,
                keywords_present,
                title_keywords_present,
            ) = get_job_details(job, parameters)
            output.append(
                [
                    rating,
                    title,
                    company,
                    description,
                    url,
                    keywords_present,
                    title_keywords_present,
                    x + 1,
                ]
            )

        print(f"Page {x+1} completed", end="\r")

    df_output_frame = (
        pd.DataFrame(
            output,
            columns=[
                "Rating",
                "Job Title",
                "Company",
                "Description",
                "Job URL",
                "Keywords Present",
                "Title Keywords",
                "Page Found",
            ],
        )
        .sort_values(by="Rating", ascending=False)
        .reset_index(drop=True)
    )

    return df_output_frame

