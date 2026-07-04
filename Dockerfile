FROM rockylinux:9.3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /agent
WORKDIR /agent

# Install system dependencies & set up repositories in a single cached layer
# Consolidating RUN commands and running 'dnf clean all' reduces the final image size.
RUN dnf install -y python3 python3-pip git 'dnf-command(config-manager)' && \
    dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    dnf install -y gh && \
    dnf install -y https://gitlab.com/gitlab-org/cli/-/releases/v1.106.0/downloads/glab_1.106.0_linux_arm64.rpm && \
    dnf clean all


RUN echo "alias ll='ls -hal'" >> /etc/bashrc && \
    echo "alias s='git status'" >> /etc/bashrc

# Copy and install Python dependencies (changes here only trigger pip reinstall)
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt --no-cache-dir -vvv

# Install agent skills for gh
RUN gh skill install cli/cli gh --scope user && \
    gh skill update gh

# Copy source code last to maximize cache efficiency
COPY src/ .

WORKDIR /opt