const HDWalletProvider = require("truffle-hdwallet-provider")
const web3 = require('web3')
const axios = require('axios')
//const ansi = require('ansicolor').nice

const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK
const DESTINATION_ADDRESS = process.env.DESTINATION_ADDRESS

// partially adapted from this tutorial https://davekiss.com/ethereum-web3-node-tutorial/


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

  console.log("\r\n")
  console.log (`Current ETH Gas Prices (in GWEI):`)
  console.log("\r\n")
  console.log(`Low: ${prices.low} (transaction completes in < 30 minutes)`)
  console.log(`Standard: ${prices.medium} (transaction completes in < 5 minutes)`)
  console.log(`Fast: ${prices.high} (transaction completes in < 2 minutes)`)
  console.log("\r\n")

  return prices
}


const main = async () => {
    const provider = new HDWalletProvider(MNEMONIC, `https://${NETWORK}.infura.io/v3/${INFURA_KEY}`)
    const web3Instance = new web3(
        provider
    )

    // web3Instance.eth.defaultAccount = OWNER_ADDRESS

    // Get the balance of the account
    // kept getting unhandled rejection errors
    // so had to add the funION(error, reults), etc.. part
    let myBalanceWei = await web3Instance.eth.getBalance(OWNER_ADDRESS,function(error,result){
        if(error){
           console.log(error)
        }
        else{
           console.log(result)
        }
      }
    )

    // convert it to eth
    let myBalance = web3Instance.utils.fromWei(myBalanceWei, 'ether')

    console.log(`Your wallet balance is currently ${myBalance} ETH`)

    // get a nonce
    let nonce = await web3Instance.eth.getTransactionCount(OWNER_ADDRESS)
    console.log(`The outgoing transaction count for your wallet address is: ${nonce}`)

    // get gas prices
    let gasPrices = await getCurrentGasPrices()

    // get amount to send

    // This will be changed (send some to hosting, then extra to me)
    // need to store some info about how much I should have and how much has been spent
    // with the hosting (maybe can check how much available, but maybe have to calculate)
    // Anyways, this is currently a POC that I can take some portion of the available
    // balance and send it.
    const amountToSend = (myBalance * 0.001).toString()
    console.log(amountToSend)

    // write transaction
    let details = {
      "to": DESTINATION_ADDRESS,
      "from": OWNER_ADDRESS,
      "value": web3Instance.utils.toHex( web3Instance.utils.toWei(amountToSend, 'ether') ),
      "gas": 21000,
      "gasPrice": gasPrices.medium * 1000000000, // converts the gwei price to wei
      "nonce": nonce,
      "chainId": 4 // EIP 155 chainId - mainnet: 1, rinkeby: 4
    }

    // send transaction
    const transactionId = await web3Instance.eth.sendTransaction(details)
    console.log("Transaction Sent")

    // exit the program
    process.exit(0);

}

main()
