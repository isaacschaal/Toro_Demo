const HDWalletProvider = require("truffle-hdwallet-provider")
const web3 = require('web3')
const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK

if (!MNEMONIC || !INFURA_KEY || !OWNER_ADDRESS || !NETWORK || !NFT_CONTRACT_ADDRESS) {
    console.error("Please set a mnemonic, infura key, owner, network, and contract address.")
    return
}

const NFT_ABI = [{
    // view is the new keyword for "constant"
    "view": false,
    "inputs": [
      {
        "name": "_to",
        "type": "address"
      }
    ],
    "name": "mintTo",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"},
    // Add to our ABI to include the returnTokenID function
    {
    // change view to true, so the return values can be accessed
    "view": true,
    "inputs": [],
    "name": "returnTokenID",
    // Specify the outputs
    "outputs": [
      {
        "name": "newTokenId",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"}
  ]

async function main() {
    const provider = new HDWalletProvider(MNEMONIC, `https://${NETWORK}.infura.io/v3/${INFURA_KEY}`)
    const web3Instance = new web3(
        provider
    )
    const nftContract = new web3Instance.eth.Contract(NFT_ABI, NFT_CONTRACT_ADDRESS, { gasLimit: "1000000" })

    // Artworks issued directly to the owner.
    const result = await nftContract.methods.mintTo(OWNER_ADDRESS).send({ from: OWNER_ADDRESS });
    console.log("Minted artwork. Transaction: " + result.transactionHash)

    // Log the TokenID
    const newTokenID = await nftContract.methods.returnTokenID().call();
    console.log("Token ID: " + newTokenID)

    // exit the program
    return process.exit(0);
}

main()
