'''
Created on 2016-5-4

@author: darcyyang
'''
num_of_agent = 5
agent_generate_file='list.txt'
# Crawler records placed file path
fileTempPath = './crapyTemp/'

# CrawlUrls
crawlUrls = [
        "",
    ]

# allowed_domains = ["dmoz.org"]
# linkEntryRule = '//*[@id="thread_6730022"]/a'

detailMainContentRule = ""

TitleRule = ""
keywordRule = ""
imageUrl = ""
downloadUrlRule = ""

#(//element[@name='D'])[last()]
lastPageNumRule = "(//div[@class='paginator']//a)[last()-1]//text()"

movieDetailPageLinkRule = "//div[@class='pl2']//a//@href"
movieTitleInDetailPageRule = "//h1//span[1]/text()"
movieYearInDetailPageRule = "//h1//span[2]/text()"
movieDirectorDetailPageRule = "//a[contains(@rel,'v:directedBy')]//text()"
movieMainStars = "//a[contains(@rel,'v:starring')]//text()"
movieGenre = "//a[contains(@rel,'v:genre')]//text()"
movieReleaseDate =  "//a[contains(@rel,'v:initialReleaseDate')]//text()"
movieRuntime = "//a[contains(@rel,'v:runtime')]//text()"
IMDBLink = "(//div[@id='info']//a)[last()]//@href"
movieLanguage = ""
movieCreationZone = ""
movieRating = "//strong[contains(@property,'v:average')]//text()"
movieCoverImage = "//div[@id='mainpic']//a//img/@src"
movieBriefDescription = "//div[@id='link-report']//span[2]//text()"




