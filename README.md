<h1 align="center">Compute mean head position across MEG runs</h1>

<p align="center">
  A destination <code>.fif</code> file holding the mean device-to-head transformation across the runs of a MEG session, for realigning all runs during Maxwell filtering.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.496"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.496-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

This App uses [MNE-Python](https://mne.tools/stable/index.html) to average the head positions recorded at the beginning of each run (`raw.info["dev_head_t"]["trans"]`) into a single transformation matrix. Passed as the destination to Maxwell filtering, this matrix realigns all runs to the mean head position.

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Computes the mean head position (device-to-head transformation matrix) across several MEG runs with MNE-Python, for realigning all runs during Maxwell filtering.**

Reads the MEG runs of a session (.fif) and averages their initial head positions into one transformation matrix, saved for use as the destination when applying Maxwell filtering so that all runs share the same head position. Use it before Maxwell filtering of multi-run MEG sessions; an optional headshape .pos file from app-head-pos can be supplied.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meg/fif` · `neuro/meg/fif-override` (optional) |
| 📤 **Outputs** | `neuro/meg/fif-override` |
| 🐳 **Container** | `brainlife/mne:0.23dev` |
| ⚙️ **Resources** | 1 CPUs |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.496](https://doi.org/10.25663/brainlife.app.496) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meg/fif` | yes | All the runs of a MEG session that we want to realign by computing the mean head position across all these runs (this position is stored in a transformation matrix). At least two runs are required. |
| `Opt` | `neuro/meg/fif-override` | no | Headshape.pos file. This file is computed with app-head-pos. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meg/fif-override` | Destination file containing the mean transformation matrix to realign all the runs on the same head position and .fif file to preprocess. |

<!-- brainlife-app:end -->

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.496](https://doi.org/10.25663/brainlife.app.496), choose all the runs of a MEG session (`neuro/meg/fif`, at least two) and, optionally, a `neuro/meg/fif-override` dataset (for example the `headshape.pos` file from the [head position App](https://github.com/brainlife/app-head-pos)), then press **Execute**. The App has no parameters. It archives a `neuro/meg/fif-override` dataset with the destination file, ready for the Maxwell filtering App.

### 💻 Locally

You need [Singularity/Apptainer](https://apptainer.org/). `main` runs `mean_transformation_matrix.py` in the `brainlife/mne:0.23dev` container.

1. Clone this repository with its helper submodule:

   ```bash
   git clone --recursive https://github.com/brainlife/app-mean-transformation-matrix.git
   ```

2. Create `config.json` with the same keys as `config.json.example`. `fif_runs` lists every run (at least two); the optional files (`headshape`, `destination`, `events`, `channels`) can be `null`:

   ```json
   {
       "fif_runs": [
           "input/rest1-raw.fif",
           "input/rest2-raw.fif"
       ],
       "headshape": null,
       "destination": null,
       "events": null,
       "channels": null
   }
   ```

3. Run the App:

   ```bash
   ./main
   ```

## 📦 Outputs

```text
out_dir/
└── destination.fif    mean transformation matrix in raw.info["dev_head_t"]["trans"]
product.json           status message shown on brainlife.io
```

Optional input files given in `config.json` are passed through to `out_dir/`.

## 🩺 Troubleshooting

- **`Only one run was given. This App needs at least two runs to compute the mean transformation matrix.`**: select two or more runs of the same session.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Compute mean head position across MEG runs. brainlife.io App. [doi:10.25663/brainlife.app.496](https://doi.org/10.25663/brainlife.app.496)
- Gramfort et al. MEG and EEG data analysis with MNE-Python. *Frontiers in Neuroscience* 7 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## 👥 Authors

- Aurore Bussalb

**Contributors:** Maximilien Chaumon, Christophe Gitton

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

[MIT](LICENSE). MNE-Python is distributed under its own BSD license.
