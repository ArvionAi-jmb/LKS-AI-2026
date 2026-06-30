#!/bin/bash
set -e

REPO_URL="https://github.com/ArvionAi-jmb/LKS-AI-2026.git"
BRANCH="main"

echo "=== Upload Sistem Prediksi Stunting ke GitHub ==="

# Cek login GitHub
if ! gh auth status &>/dev/null; then
    echo "Kamu belum login ke GitHub. Login dulu..."
    echo ""
    echo "Pilih metode login:"
    echo "1) Login via browser (default)"
    echo "2) Login via token (PAT)"
    read -rp "Pilihan [1/2]: " method
    if [ "$method" = "2" ]; then
        echo ""
        echo "Masukkan Personal Access Token (classic) dengan repo scope:"
        echo "Buat token di https://github.com/settings/tokens"
        read -rsp "Token: " token
        echo ""
        echo "$token" | gh auth login --with-token
    else
        gh auth login
    fi
    echo ""
fi

# Init git kalo belum
if [ ! -d ".git" ]; then
    echo "Init repository..."
    git init
fi

# Set git config lokal kalo global belum terisi
if ! git config --global user.name &>/dev/null; then
    read -rp "Masukkan nama GitHub: " git_name
    git config user.name "$git_name"
fi
if ! git config --global user.email &>/dev/null; then
    read -rp "Masukkan email GitHub: " git_email
    git config user.email "$git_email"
fi

# Cek remote
if ! git remote get-url origin &>/dev/null; then
    echo "Tambah remote origin..."
    git remote add origin "$REPO_URL"
else
    git remote set-url origin "$REPO_URL"
fi

# Stage semua file
git add .

# Commit
echo "Buat commit..."
git commit -m "Initial commit - Sistem Monitoring & Prediksi Stunting"

# Push
echo "Push ke $BRANCH..."
git branch -M "$BRANCH"
git push -u origin "$BRANCH"

echo ""
echo "=== Berhasil! ==="
echo "Repo: $REPO_URL"
