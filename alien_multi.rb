#!/usr/bin/env ruby

# Name: alien_oauth.rb
# Description: Grab subreddits corresponding to a user's multireddit
# Author: Bob Gardner
# Updated: 8/19/15
# License: MIT

require 'redd'
require 'optparse'

module AlienWallpaper

  VERSION = '0.0.2'
  USER_AGENT = "Alien Wallpaper v#{VERSION} by /u/Wolf_Blackout"

  class MultiReddit

    CLIENT_ID = ENV['REDDIT_CLIENT_ID']
    SECRET = ENV['REDDIT_SECRET']

    def self.cli_options
      options = {}
      optparse = OptionParser.new do |opts|
        opts.on('-u', '--username USER', String, 'Reddit username') do |u|
          options[:u] = u
        end
        opts.on('-p', '--password PASS', String, 'Reddit password') do |p|
          options[:p] = p
        end
        opts.on('-m', '--multi MULTI', String, 'Multireddit name') do |m|
          options[:m] = m
        end
      end
      optparse.parse!
      options
    end

    def self.main
      opts = cli_options
      r = self.authorize(CLIENT_ID, SECRET, opts[:u], opts[:p], USER_AGENT)
      multis = r.multi_from_path("/user/#{opts[:u]}/m/#{opts[:m]}")
      puts multis.subreddits.join(',')
    end

    private

    def self.authorize(client_id, secret, username, password, user_agent)
      r = Redd.it(:script, client_id, secret, username, password,
                  user_agent: user_agent)
      r.authorize!
      r
    end
  end
end

AlienWallpaper::MultiReddit.main
