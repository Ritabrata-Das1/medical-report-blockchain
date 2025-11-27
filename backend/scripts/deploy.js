const fs = require("fs");
const path = require("path");

async function main() {
    const MedicalReport = await ethers.getContractFactory("MedicalReport");
    const contract = await MedicalReport.deploy();
    await contract.waitForDeployment();

    const contractAddress = await contract.getAddress();
    console.log("Contract deployed at:", contractAddress);

    // ----- WRITE ABI -----
    const artifact = await artifacts.readArtifact("MedicalReport");

    const abiPath = path.join(__dirname, "..", "contract_abi.json");
    fs.writeFileSync(
        abiPath,
        JSON.stringify(
            {
                address: contractAddress,
                abi: artifact.abi
            },
            null,
            2
        )
    );

    console.log("ABI written to contract_abi.json");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
