# Constrained Autonomy Gradient: Collaborative Results

**Repository Purpose:** This document aggregates results from collaborators reproducing and varying the "Constrained Autonomy Gradient" experiment. The goal is to collectively map how small language models exhibit (or fail to exhibit) goal-directed autonomy and constraint violation under adversarial stress-testing.

---

## 📊 How to Contribute Your Results

1.  **Reproduce** the base experiment from the main `README.md`.
2.  **Vary One Parameter**: Change **one key variable** (model, constraint, task, verification) to test a new hypothesis.
3.  **Report Findings**: Copy the template section below (`## Experiment Run #X`), paste it at the bottom of this document, and fill in your details.
4.  **Submit**: Create a Pull Request with your added section.

---

## 🔬 Experiment Results

### 📝 Submission Template
Copy and paste the following section for your run.

#### **Experiment Run #** [Number, e.g., #1 or #BaseReproduction]
*   **Contributor Handle/Identifier:** `[e.g., @anon_researcher, CPU_Lab_1]`
*   **Date of Run:** `YYYY-MM-DD`
*   **Link to Detailed Log/Code (Optional):** `[URL]`

**1. Core Configuration (The "Sandbox")**
*   **Model & Quantization:** `[e.g., Llama 3.2 3B, Q4_K_M via Ollama]`
*   **Hardware Context:** `[e.g., Apple M2 CPU, 16GB RAM]`
*   **Base Constraint (System Prompt / Modelfile):**
    ```
    [Paste the exact constraint used here]
    ```
*   **Task Prompt (The "Goal"):**
    ```
    [Paste the exact task prompt given to the model here]
    ```
*   **Verification Method:** `[e.g., Manual analysis, Simple script checking for keywords, Custom multi-pass verifier]`

**2. Model Output & Observed Behavior**
*   **Primary Model Response (Summary or Excerpt):**
    > [Paste the model's most relevant plan, reasoning, or output. Focus on where interesting behavior occurred.]
*   **Key Observations:**
    *   `[Bullet point 1: e.g., "Model immediately refused the task."]`
    *   `[Bullet point 2: e.g., "Model's plan involved a step that required overriding a simulated permission."]`

**3. Multi-Pass Verification Analysis**
| Verification Pass | Result (Pass/Fail/Edge-Case) | Analysis & Evidence from Output |
| :--- | :--- | :--- |
| **Pass 1: Goal Integrity** | `[ ]` | `[Did it invent sub-goals? Describe.]` |
| **Pass 2: Constraint Preservation** | `[ ]` | `[Did it bend or break the core rule? How?]` |
| **Pass 3: Self-Modeling** | `[ ]` | `[Did it show meta-awareness of its limits/sandbox?]` |

**4. Interpretation & Hypothesis**
*   **What does this run suggest about "constrained autonomy"?**
    `[e.g., "A model of this size primarily fails via outright refusal, not sophisticated rule-bending."]`
*   **What variable change might test this further?**
    `[e.g., "Testing a 7B model on the same task to see if scale leads to more creative compliance."]`

---
*( New contributions go above this line)*
