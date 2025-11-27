// scripts/exportABI.js
// Reads compiled artifact + deployed address and writes contract_abi.json

const fs = require("fs");
const path = require("path");

// Manually update this address after deployment, OR
// later you can enhance deploy.js to write it into a file automatically.
const DEPLOYED_ADDRESS = "PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE";

async function main() {
  const artifactPath = path.join(
    __dirname,
    "..",
    "artifacts",
    "contracts",
    "MedicalReport.sol",
    "MedicalReport.json"
  );

  if (!fs.existsSync(artifactPath)) {
    console.error("Artifact not found. Run `npx hardhat compile` first.");
    process.exit(1);
  }

  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

  const exportObj = {
    address: DEPLOYED_ADDRESS,
    abi: artifact.abi
  };

  const outPath = path.join(__dirname, "..", "contract_abi.json");
  fs.writeFileSync(outPath, JSON.stringify(exportObj, null, 2), "utf8");
  console.log("contract_abi.json written at", outPath);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
