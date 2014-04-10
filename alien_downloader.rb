#!/usr/bin/env ruby

# Name: downloader.rb
# Description: Downloads top 25 images from specified subreddits.
# Author: Bob Gardner
# Updated: 4/9/14
# License: MIT

require 'open-uri'
require 'snoo'
require 'yaml'

CONFIG     = YAML.load_file(File.expand_path('../config/preferences.yaml',
                                             __FILE__))
LOGIN_INFO = YAML.load_file(File.expand_path('../config/reddit_account.yaml',
                                             __FILE__))
# The directory to download images to
OUTPUT_DIR = Dir.new(CONFIG['output_dir'])

# Supported file types
FILE_EXTENSION_REGEX = /\.(jpg|jpeg|gif|png)$/i

# The subreddits to download images from.
SUBREDDITS = %w(ArchitecturePorn CityPorn EarthPorn SkyPorn spaceporn
                winterporn quoteporn)

# Download images from Reddit
class Downloader
  attr_accessor :reddit

  # Returns a reddit client
  def create_client
    @reddit = Snoo::Client.new
    @reddit.log_in(LOGIN_INFO['username'], LOGIN_INFO['password'])
  end

  # Returns a post Hash
  def get_posts(subreddit)
    opts = { subreddit: "#{subreddit}", page: 'new', limit: 25 }
    listing = @reddit.get_listing(opts)
    listing['data']['children']
  end

  # Save the invalid url to invalid-urls.log
  def log_invalid_url(url)
    File.open('invalid-urls.log', 'a') do |log|
      log.write("#{url}\n")
    end
  end

  # Skip nil and self posts, log unsupported urls, and save valid, supported
  # images
  def process_post(post)
    # Skip nil and self posts
    return if post.nil?
    return if post['data']['domain'].start_with?('self')

    # Log unsupported file types
    unless post['data']['url'].match(FILE_EXTENSION_REGEX)
      log_invalid_url(post['data']['url'])
      return
    end

    download_image(post)
  end

  def download_image(post)
    # Construct the filename and filepath
    filename = post['data']['id'] +
               post['data']['url'].match(FILE_EXTENSION_REGEX)[0]
    filepath = File.join(OUTPUT_DIR, filename)
    puts filepath

    # Need to use write-binary (wb) mode for images
    File.open(filepath, 'wb') do |f|
      f << open(post['data']['url']).read
    end
  end

  def main
    create_client
    SUBREDDITS.each do |subreddit|
      posts = get_posts(subreddit)
      posts.each { |post| process_post(post) }
    end
  end
end

if __FILE__ == $PROGRAM_NAME
  x = Downloader.new
  x.main
end

# def handle_flickr(href)
#   unless href.index('/sizes')
#     in_position = href.index('/in/')
#     in_fragment = ''
#     if in_position != -1
#       in_fragment = href.slice(inPosition)
#       href = href.slice(0, inPosition)
#     end
#     href += '/sizes/c' + in_fragment
#   end
#   href.gsub!('/lightbox', '')
#   href = 'http://www.flickr.com/services/oembed/?format=json&url=' + href
# end
