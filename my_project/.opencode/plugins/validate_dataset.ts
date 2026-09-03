/// <reference types="node" />

import { existsSync } from "node:fs"
import { isAbsolute, relative, resolve } from "node:path"
import { tool, type Plugin } from "@opencode-ai/plugin"

const validateDatasetPlugin: Plugin = async ({ $, directory, worktree }) => {
  return {
    tool: {
      validate_dataset: tool({
        description: "Validate a CSV dataset and return a JSON report with errors and warnings.",
        args: {
          filepath: tool.schema.string().describe("Path to the CSV file, relative to the project directory"),
        },
        async execute({ filepath }) {
          const datasetPath = isAbsolute(filepath) ? resolve(filepath) : resolve(directory, filepath)
          const worktreePath = resolve(worktree)
          const pathFromWorktree = relative(worktreePath, datasetPath)

          if (pathFromWorktree.startsWith("..") || isAbsolute(pathFromWorktree)) {
            return "Error: filepath must point to a file inside the project worktree."
          }

          const scriptCandidates = [
            resolve(worktreePath, "hf-dataset-validation/scripts/validate_dataset.py"),
            resolve(worktreePath, "../hf-dataset-validation/scripts/validate_dataset.py"),
          ]
          const scriptPath = scriptCandidates.find((candidate) => existsSync(candidate))

          if (!scriptPath) {
            return "Error: could not find hf-dataset-validation/scripts/validate_dataset.py."
          }

          const result = await $.nothrow()`python3 ${scriptPath} ${datasetPath}`.quiet()
          const output = result.text().trim()

          if (result.exitCode !== 0) {
            return output || `Validation failed with exit code ${result.exitCode}.`
          }

          return output
        },
      }),
    },
  }
}

export default validateDatasetPlugin