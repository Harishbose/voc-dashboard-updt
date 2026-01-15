# VOC Dashboard - Automated Data Processing Guide

## Monthly Data Update Process

### What You Need to Do:
Simply upload the new raw data file to GitHub!

### Step-by-Step:

1. **Prepare your data**
   - Get your raw data file (latest_t.csv or latest_t.xlsx)
   - Make sure the file has the same columns as before

2. **Upload to GitHub**
   - Go to https://github.com/Harishbose/voc-dashboard-updt
   - Click "Upload files" button
   - Upload your `latest_t.csv` file
   - Commit with message like: "Monthly data update - January 2026"

3. **Automation Happens Automatically** ✅
   - GitHub Actions detects the new file
   - Runs the processing pipeline
   - Maps data with store information
   - Fixes city names
   - Cleans columns
   - Generates cleaned CSV files
   - Auto-commits the results back to GitHub

4. **Render Updates Automatically** ✅
   - Render detects the new processed files
   - Redeploys your dashboard
   - Your live dashboard gets updated within 5-10 minutes

### Files Involved:

**Input:**
- `latest_t.csv` - Your raw monthly data (upload this)
- `STORE_LIST MAPPING.xlsx` - Store reference data (stays same)

**Processing:**
- `process_data.py` - Automated processing script
- `.github/workflows/process-data.yml` - GitHub Actions workflow

**Outputs (auto-generated):**
- `latest_t_mapped.csv` - Mapped with store info
- `latest_t_mapped_clean.csv` - Clean final version
- These are used by your dashboard

### What Happens in Processing:

1. ✓ Loads your raw `latest_t.csv` data
2. ✓ Maps it with store names, locations, tiers, zones
3. ✓ Fixes common city name variations
4. ✓ Removes unnecessary columns
5. ✓ Generates clean CSV for dashboard
6. ✓ Auto-commits changes

### Dashboard Updates:

After you upload `latest_t.csv`:
- GitHub Action runs immediately (visible in Actions tab)
- Processing takes ~2-3 minutes
- Results committed automatically
- Render detects changes
- Dashboard refreshes within 10 minutes
- **Your live dashboard is updated!** 🎉

### Troubleshooting:

**If processing fails:**
- Check the GitHub Actions tab for error details
- Ensure your CSV has the correct columns
- Verify store names match the mapping file

**If dashboard doesn't update:**
- Check Render's deployment log
- Give it 10 minutes max
- Restart manually if needed on Render dashboard

### Manual Testing:

To test locally before uploading:
```bash
# Place your latest_t.csv in the folder
# Run the processing script
python process_data.py

# Check the outputs
# latest_t_mapped.csv and latest_t_mapped_clean.csv should be created
```

## Security Note

**IMPORTANT**: This workflow uses GitHub's built-in `GITHUB_TOKEN` which is automatically provided and secure. No personal access tokens are stored in code or configuration files.
