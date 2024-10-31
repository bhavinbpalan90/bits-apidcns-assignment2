# Text based Database Search

Purpose of this Utility is to search the data from the Database and Respond in a Natural Language.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

---

## Project Overview

This Project is designed to respond User Inputs for a search of data from database tables.

## Features

- Feature 1: Text based Search from the Database Tables.
- Feature 2: Generate LLM Respond in a Natural Language.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bhavinbpalan90/text-to-db-search.git
   cd text-to-db-search

2. **Setup Conda Environment & Packages**

    conda create --name <envName>
    conda activate <envName>

    pip install -r requirements.txt

## Usage

1. **Update OpenAI API Key before Proceeding further**

    1. Login in Open AI Platform to generate the API Key.
    2. Update the key in .env file in the placeholder.

2. **Execute Python to get Response**

    1. Modify Sample question in main.py (Please be aware of the data in bits.db)
    2. execute python main.py
