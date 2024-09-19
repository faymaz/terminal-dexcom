# Dexcom Blood Glucose Monitoring with Zsh Prompt Integration

![Dexcom_1](images/dexcom_1.png)

This project allows you to display **live blood glucose (BG) values** from a **Dexcom CGM (Continuous Glucose Monitoring)** device directly in your **Zsh prompt**. The BG values are dynamically updated in the prompt along with the current time, providing real-time glucose monitoring directly in your terminal.

## Features

- **Dynamic BG Values in Terminal Prompt**: The Zsh prompt displays your current blood glucose values, trend arrows, and time.
- **Color-Coded Glucose Levels**:
  - **Red** for low BG values (below 90 mg/dL).
  - **Green** for normal BG values (90-160 mg/dL).
  - **Yellow** for elevated BG values (above 160 mg/dL).
- **Auto-Refresh**: The prompt refreshes automatically every 5 seconds with the latest BG values.
- **Background Python Script**: A Python script fetches BG data from Dexcom every 5 minutes and stores it for the terminal to display.

## Requirements

- **macOS** (with Zsh as the default shell).
- **Dexcom Developer Account**: You need Dexcom API credentials.
- **Python 3.x** installed on your system.

### Python Libraries

- `pydexcom`
- `requests`

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/faymaz/dexcom.git
cd dexcom
```

### Step 2: Install Required Python Libraries

Install the required Python libraries using `pip`:

```bash
pip install pydexcom requests
```
![Dexcom_2](images/Dexcom_2.png)

### Step 3: Configure Dexcom API Credentials

You need to configure your Dexcom API credentials. Open the `dexcom_reader.py` file and replace the placeholders with your **Dexcom username** and **password**:

```python
dexcom = Dexcom(username="your_email_or_phone", password="your_password", ous=True)
```

### Step 4: Set Up the Zsh Prompt

Add the following code to your `.zshrc` file to dynamically update the Zsh prompt with BG values and time:

```bash
# BG Value and Time Prompt for Zsh
bg_info_file="/tmp/bg_info.txt"

function get_bg_info {
    if [[ -f "$bg_info_file" ]]; then
        cat "$bg_info_file"
    else
        echo -n ""  # Empty if no BG info is available
    fi
}

function get_time {
    echo "$(date '+%H:%M:%S')"  # Displays the current time in HH:MM:SS format
}

function update_prompt {
    PROMPT="$(get_bg_info) $(get_time) %n@%m:%~$ "
}

TRAPALRM() {
    update_prompt
}

ALRM_INTERVAL=5
autoload -U add-zsh-hook
add-zsh-hook precmd () {
    update_prompt
    [[ $ALRM_INTERVAL -gt 0 ]] && sleep $ALRM_INTERVAL && kill -ALRM $$
}
```

After adding this to your `.zshrc`, apply the changes:

```bash
source ~/.zshrc
```

### Step 5: Run the Python Script

Run the Python script in the background to fetch BG values:

```bash
python3 dexcom_reader.py &
```

This script will run in the background, fetching your glucose readings from the Dexcom API every 5 minutes and writing the data to `/tmp/bg_info.txt`. Your Zsh prompt will automatically refresh every 5 seconds to display the latest BG data and time.

## Usage

Once everything is set up, your terminal prompt will display your blood glucose levels along with the current time.

Example prompt:

```bash
163 mg/dL → 14:25 faymaz@programirez:~/Projects/dexcom$
```

### Color Codes

- **Red** for BG values below 90 mg/dL.
- **Green** for BG values between 90 and 160 mg/dL.
- **Yellow** for BG values above 160 mg/dL.

### Customization

You can adjust the refresh interval for the Zsh prompt by changing the `ALRM_INTERVAL` value in the `.zshrc` file. For example, setting `ALRM_INTERVAL=10` will refresh the prompt every 10 seconds.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
