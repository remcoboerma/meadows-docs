FROM educationwarehouse/edwhale-3.13:latest

RUN apt install git
RUN uvenv install --no-cache mkdocs
RUN uvenv inject --no-cache mkdocs mkdocs-material
RUN uvenv inject --no-cache mkdocs cairosvg pillow
RUN uvenv inject --no-cache mkdocs mkdocs-git-revision-date-localized-plugin
RUN uvenv inject --no-cache mkdocs mkdocs-git-committers-plugin-2

WORKDIR /docs
COPY docs/ /docs/

CMD ["/root/.local/bin/mkdocs", "serve", "--dev-addr", "0.0.0.0:8000"]
