#!/usr/bin/env ruby

# Name: alien_wallpaper.rb
# Description: Downloads top 25 images from specified subreddits.
# Author: Bob Gardner
# Updated: 8/23/14
# License: MIT

require 'open-uri'
require 'snoo'
require 'trollop'

# The default subreddits to download images from.
DEFAULT_SUBREDDITS = <<-EOS
ArchitecturePorn,CityPorn,EarthPorn,SkyPorn,spaceporn,winterporn,quoteporn
EOS

USER_AGENT = <<-EOS
Alien Wallpaper: A beautiful desktop wallpaper downloader for Reddit by
/u/Wolf_Blackout.
EOS

# Supported file types.
FILE_EXTENSION_REGEX = /\.(jpg|jpeg|gif|png)$/i


class Client
  attr_accessor :client

  # Initialize and log in the client.
  def initialize
    @client = Snoo::Client.new({ useragent: USER_AGENT })
  end

  # Returns a post hash.
  def get_posts(subreddit, num_posts)
    opts = { subreddit: "#{subreddit}", page: 'new', limit: num_posts }
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
      $stderr.puts post['data']['url']
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
end

def get_opts
  Trollop.options do
    banner 'Download Wallpaper from Subreddits'
    opt :n, 'Number of images to download for each subreddit', default: 25
    opt :out, 'Directory to save wallpaper to', default: Dir.pwd
    opt :subreddits, 'Comma separated subreddits to download images from; ' \
         'the defaults are SFW', default: DEFAULT_SUBREDDITS.strip
  end
end

def main
  opts = get_opts
  client = Client.new

  opts[:subreddits].split(',').each do |subreddit|
    posts = client.get_posts(subreddit, opts[:n])
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
