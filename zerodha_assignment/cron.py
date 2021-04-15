from populate import clean_folder,get_url,get_filename,download_zip,get_csv,populatedb,populate_cache
def my_cron_job():
    url=get_url()
    download_zip(url)
    clean_folder()
    get_csv('file.zip')
    populatedb()
    populate_cache()
