#!/usr/bin/env ruby
=begin
  * Name: downloader.rb
  * Description: Downloads top 25 images from specified subreddits
  * Author: Bob Gardner
  * Date: 11/27/13
  * License: MIT
=end

require 'open-uri'
require 'snoo'

CONFIG     = YAML.load_file(File.expand_path('../config/preferences.yaml',
                            __FILE__))
LOGIN_INFO = YAML.load_file(File.expand_path('../config/reddit_account.yaml',
                            __FILE__))

FILE_EXTENSION_REGEX = /(\.\w{3,})$/

OUTPUT_DIR = Dir.new(CONFIG["output_dir"])
SUBREDDITS = [ 'ArchitecturePorn', 'CityPorn', 'EarthPorn', 'SkyPorn',
               'spaceporn', 'winterporn', 'quoteporn' ]

reddit = Snoo::Client.new
reddit.log_in LOGIN_INFO['username'], LOGIN_INFO['password']

SUBREDDITS.each do |subreddit|
  opts = { subreddit: "#{subreddit}", page: "new", limit: 25 }
  listing = reddit.get_listing(opts)
  posts = listing["data"]["children"]
  posts.each do |post|
    next if post.nil?
    next if post["data"]["domain"] == "self.#{subreddit}"
    next if post["data"]["url"].match(FILE_EXTENSION_REGEX).nil?

    filename = post["data"]["id"] +
               post["data"]["url"].match(FILE_EXTENSION_REGEX)[0]
    filepath = File.join(OUTPUT_DIR, filename)
    puts filepath
    File.open(filepath, "wb") do |fo|
      fo.write open(post["data"]["url"]).read
    end
  end
end
