# Canvas Scraper

Well this project is a bit of a mess at the moment!  

## About

### The what
 
 This is a python tool which downloads files from Canvas. Currently, it only supports downloading files listed in the files section and files listed in the modules section. Support will widen as I encounter more derangedly-arranged classes. 

### The why

Your college might use Canvas; if you're here, it almost definitely does. However, Canvas is not very good! Its goal is to centralise and digitise class materials and information, but all it really does is spread theme across a slow, ugly (in my opinion), innavigable, and inconstant (one of my classes has a modules section but no files section; another has a files section but no modules section) interface! Thus I conclude Canvas to be a great evil.  
For me, the best way to centralise files and render them most accessible is to have them well-named and sorted into a nice, nested, equally well-named folder on my nice, organised filesystem, which allows them to be accessed in a nearly infinite number of ways. To get to such a point, I need to download the files from Canvas. Obviously, downloading massive amounts of files from Canvas (50+) is one of the less desirable ways to place one's self into mental-reconstruction institutions, and I didn't particularly want that to be a byproduct of my college experience. Hence, I made a command-line tool which downloads them for me! And it's not easy to put a command-line tool into a mental-reconstruction institution!

## Usage
* You'll need Python (3), BeautifulSoup, and Playwright. Sorry about that.
  * Beautiful Soup and Playwright should both be installable through PIP.
  * Your distribution may also have some of these packages in the official repositories.
	  * If you are on Arch Linux, you should install Playwright this way
* You'll also need a `cookies.json` in the same directory as the script.
* Lastly, you'll need the URL of the class' "files" or "modules" section . 
  * Not all classes have a "files" section made available; some will even nix the "modules" section as well, while still making Canvas-hosted files available in some dark corner of the interface. If you find such an example, please send me the HTML for the page which indexes the files so I can expand this project with capabilities to scrape from such a source.

## Invokation
`python3 main.py [URL]`
`python3 modules.py [URL]`

  
## Contributing
Open an issue, make a pull request, etc. 

## Future of this project
I hope to abstract the primary functions into their own library and unify the scraping scripts (there really is no need to use multiple scripts, is there?)
I'll probably make the UX a bit better by adding more customisability (i.e., downloading files from the class' ID alone, support of cookie files in arbitrary locations, support for specification of download folder, etc.).
However, I am in college (busy!) so it is not particularly likely that any of these things will occur before a need is expressed for them. 
