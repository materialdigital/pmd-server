FROM jekyll/jekyll:latest
COPY Gemfile /srv/jekyll/
RUN bundle install
CMD bundle exec jekyll serve
