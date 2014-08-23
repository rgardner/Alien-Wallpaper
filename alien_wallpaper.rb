#!/usr/bin/env ruby

# Name: alien_wallpaper.rb
# Description: Downloads top 25 images from specified subreddits.
# Author: Bob Gardner
# Updated: 8/23/14
# License: MIT

require 'open-uri'
require 'snoo'
require 'trollop'

# The subreddits to download images from.
DEFAULT_SUBREDDITS = %w(ArchitecturePorn CityPorn EarthPorn SkyPorn spaceporn
                        winterporn quoteporn)

# Supported file types.
FILE_EXTENSION_REGEX = /\.(jpg|jpeg|gif|png)$/i


class Client
  attr_accessor :client

  # Initialize and log in the client.
  def initialize(username, password)
    @client = Snoo::Client.new
    @client.log_in(username, password)
  end

  # Returns a post hash.
  def get_posts(subreddit)
    opts = { subreddit: "#{subreddit}", page: 'new', limit: 25 }
    listing = @client.get_listing(opts)
    listing['data']['children']
  end
end

class Post

  # Skip nil and self posts, log unsupported urls, and save valid, supported
  #   images.
  def self.process_post(post, output_dir)
    # Skip nil and self posts
    return if post.nil?
    return if post['data']['domain'].start_with?('self')

    # Log unsupported file types
    unless post['data']['url'].match(FILE_EXTENSION_REGEX)
      log_invalid_url(post['data']['url'])
      return
    end

    download_image(post, output_dir)
  end

  private

  def self.download_image(post, output_dir)
    # Construct the filename and filepath
    filename = post['data']['id'] +
               post['data']['url'].match(FILE_EXTENSION_REGEX)[0]
    filepath = File.join(output_dir, filename)
    puts filepath

    # Need to use write-binary (wb) mode for images
    File.open(filepath, 'wb') do |f|
      f << open(post['data']['url']).read
    end
  end

  # Save the invalid url to invalid-urls.log
  def self.log_invalid_url(url)
    File.open('invalid-urls.log', 'a') do |log|
      log.write("#{url}\n")
    end
  end
end

def main
  opts = Trollop.options do
    banner 'Download Wallpaper from Subreddits'
    opt :n,       'Number of images to download for each subreddit', type: :int
    opt :out,     'Directory to save wallpaper to', type: :string
    opt :password, 'Your Reddit password', type: :string
    opt :subreddits, 'Comma separated subreddits to download images from',
         type: :string
    opt :username,   'Your Reddit username', type: :string
  end

  if opts[:subreddits]
    subreddits = opts[:subreddits].split(',')
  else
    subreddits = DEFAULT_SUBREDDITS
  end
  client = Client.new(opts[:username], opts[:password])

  subreddits.each do |subreddit|
    posts = client.get_posts(subreddit)
    posts.each { |post| Post.process_post(post, opts[:out]) }
  end
end

main

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
