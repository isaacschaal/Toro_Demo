// This script mints a new token
// It is called by the main_mint.py function

// It mints a token with ID which is 1 greater
// than the previously minted token, so requires no
// arguments. The token metadata is linked to the id
// and is uploaded in a seperate function in the main_mint.py script

///////////////////

// Access our environement variables
const HDWalletProvider = require("truffle-hdwallet-provider")
const web3 = require('web3')
const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK

// Ensure that we have all environment variables
if (!MNEMONIC || !INFURA_KEY || !OWNER_ADDRESS || !NETWORK || !NFT_CONTRACT_ADDRESS) {
    console.error("Please set a mnemonic, infura key, owner, network, and contract address.")
    return
}

// Define our ABI
const NFT_ABI = [{
    // View is the new keyword for "constant"
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
    // Change view to true, so the return values can be accessed
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

// The main minting function
async function main() {

    // Connect to our wallet and create a web3Instance
    const provider = new HDWalletProvider(MNEMONIC, `https://${NETWORK}.infura.io/v3/${INFURA_KEY}`)
    const web3Instance = new web3(
        provider
    )
    // Connect to our contract
    const nftContract = new web3Instance.eth.Contract(NFT_ABI, NFT_CONTRACT_ADDRESS, { gasLimit: "1000000" })

    // Issue an artwork directly to the owner.
    const result = await nftContract.methods.mintTo(OWNER_ADDRESS).send({ from: OWNER_ADDRESS });
    console.log("Minted artwork. Transaction: " + result.transactionHash)

    // Log the TokenID
    const newTokenID = await nftContract.methods.returnTokenID().call();
    console.log("Token ID: " + newTokenID)

    // Exit the program
    return process.exit(0);
}

main()
