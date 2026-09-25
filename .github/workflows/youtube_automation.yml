name: YouTube Abyss Ultimate Automation

on:
  schedule:
    - cron: '0 13 * * *'
    - cron: '0 16 * * *'
  workflow_dispatch:
    inputs:
      mode:
        description: 'Qaysi format ishga tushsin?'
        required: true
        default: 'shorts'
        type: choice
        options:
          - shorts
          - long_3min
          - series_4min
          - post

jobs:
  build-and-upload:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install google-genai google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 pillow moviepy==1.0.3 edge-tts requests numpy

      - name: Determine Mode and Execute
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          YOUTUBE_TOKEN_JSON: ${{ secrets.YOUTUBE_TOKEN_JSON }}
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            SELECTED_MODE="${{ github.event.inputs.mode }}"
          else
            SELECTED_MODE="shorts"
          fi
          echo "🚀 ISHGA TUSHIRILAYOTGAN REJIM: $SELECTED_MODE"
          python run.py --mode=$SELECTED_MODE

      - name: Commit & Push History
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add history.json
          git commit -m "Auto-update video history [skip ci]" || exit 0
          git push
