// This function sends ETH to the address specified in the
// DESTINATION_ADDRESS line of the .env file

// Currently, this function sends 1% of the ETH the wallet contains
// This is used to demonstrate the capability of sending ETH to a
// specific address, based on the amount of  ETH the wallet currently holds

// It could be easily adjusted to send ETH to an address that pays for the server hosting
// As this implementation is on a test Network, I am not sending ETH to the
// server provider but instead to myself, and manually sending real (non-test) ETH
// to the hosting service

// Partially adapted from this tutorial https://davekiss.com/ethereum-web3-node-tutorial/

// Load our modules
const HDWalletProvider = require("truffle-hdwallet-provider")
const web3 = require('web3')
const axios = require('axios')

// Access our environement variables
const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK
const DESTINATION_ADDRESS = process.env.DESTINATION_ADDRESS

// Ensure that we have all environment variables
if (!MNEMONIC || !INFURA_KEY || !OWNER_ADDRESS || !NETWORK || !NFT_CONTRACT_ADDRESS) {
    console.error("Please set a mnemonic, infura key, owner, network, and contract address.")
    return
}

/**
 * Fetch the current transaction gas prices from https://ethgasstation.info/
 *
 * @return {object} Gas prices at different priorities
 */
const getCurrentGasPrices = async () => {
  let response = await axios.get('https://ethgasstation.info/json/ethgasAPI.json')
  let prices = {
    low: response.data.safeLow / 10,
    medium: response.data.average / 10,
    high: response.data.fast / 10
  }
  return prices
}

// Main function for sending ETH
const main = async () => {
    const provider = new HDWalletProvider(MNEMONIC, `https://${NETWORK}.infura.io/v3/${INFURA_KEY}`)
    const web3Instance = new web3(
        provider
    )

    // Get the balance of the account
    let myBalanceWei = await web3Instance.eth.getBalance(OWNER_ADDRESS,function(error,result){
        if(error){
           console.log(error)
        }
        else{
           console.log(result)
        }
      }
    )

    // Convert it to eth
    let myBalance = web3Instance.utils.fromWei(myBalanceWei, 'ether')

    console.log(`Your wallet balance is currently ${myBalance} ETH`)

    // Get a nonce
    let nonce = await web3Instance.eth.getTransactionCount(OWNER_ADDRESS)
    console.log(`The outgoing transaction count for your wallet address is: ${nonce}`)

    // Get gas prices
    let gasPrices = await getCurrentGasPrices()

    // Get amount to send

    // Currently, this sends 1% of the ETH in the wallet
    // To send a specific amount of ETH (such as how much is
    // is needed to pay for server hosting), it can be specified here
    const amountToSend = (myBalance * 0.001).toString()
    console.log(amountToSend)

    // Write transaction
    let details = {
      "to": DESTINATION_ADDRESS,
      "from": OWNER_ADDRESS,
      "value": web3Instance.utils.toHex( web3Instance.utils.toWei(amountToSend, 'ether') ),
      "gas": 21000,
      "gasPrice": gasPrices.high * 1000000000, // Converts the gwei price to wei
      "nonce": nonce,
      "chainId": 4 // EIP 155 chainId - mainnet: 1, rinkeby: 4
    }

    // Send transaction
    const transactionId = await web3Instance.eth.sendTransaction(details)
    console.log("Transaction Sent")

    // Exit the program
    process.exit(0);

}

main()
