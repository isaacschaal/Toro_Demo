// This script starts an english auction for
// a token.
// It is called by the main_mint.py function

// It takes as arugment the tokenID and the
// number of favorites the artwork recieved, to
// set the minimum price

// Connect to the OpenSea-SDK, import our other modules
const opensea = require('opensea-js')
const OpenSeaPort = opensea.OpenSeaPort;
const Network = opensea.Network;
const MnemonicWalletSubprovider = require('@0x/subproviders').MnemonicWalletSubprovider
const RPCSubprovider = require('web3-provider-engine/subproviders/rpc')
const Web3ProviderEngine = require('web3-provider-engine')
const ArgumentParser = require('argparse').ArgumentParser;

// Access our environement variables
const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK

// Ensure that we have all environment variables
if (!MNEMONIC || !INFURA_KEY || !NETWORK || !OWNER_ADDRESS) {
    console.error("Please set a mnemonic, infura key, owner, network, and owner adress.")
    return
}

if ( !NFT_CONTRACT_ADDRESS) {
    console.error("Please set a NFT contract address.")
    return
}

// Create arg parser
var parser = new ArgumentParser({
  version: '0.0.1',
  addHelp:true,
  description: 'Argparser'
});
parser.addArgument(
  [ '-f', '--favorites' ],
  {
    help: 'count of favorites'
  }
);
parser.addArgument(
  [ '-i', '--id' ],
  {
    help: 'token id'
  }
);
const args = parser.parseArgs()

// For our Mnemonic Wallet
const BASE_DERIVATION_PATH = `44'/60'/0'/0`

// Connect to our wallet through Infura
const mnemonicWalletSubprovider = new MnemonicWalletSubprovider({ mnemonic: MNEMONIC, baseDerivationPath: BASE_DERIVATION_PATH})
const infuraRpcSubprovider = new RPCSubprovider({
    rpcUrl: 'https://' + NETWORK + '.infura.io/v3/' + INFURA_KEY,
})

const providerEngine = new Web3ProviderEngine()
providerEngine.addProvider(mnemonicWalletSubprovider)
providerEngine.addProvider(infuraRpcSubprovider)
providerEngine.start();

// Connect to the OpenSeaPort
const seaport = new OpenSeaPort(providerEngine, {
    networkName: NETWORK === 'mainnet' ? Network.Main : Network.Rinkeby
}, (arg) => console.log(arg))

async function main() {

    // Creat an English auction.
    console.log("English auctioning an item in DAI...")
    const wethAddress = NETWORK == 'mainnet' ? '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' : "0xc778417e063141139fce010982780140aa0cd5ab"
    // Auction for one day ( Can change to another length of time here)
    const expirationTime = Math.round(Date.now() / 1000 + 60 * 60 * 24)

    // Create the sell order
    const englishAuctionSellOrder = await seaport.createSellOrder({
        asset: {
            tokenId: String(args['id']),
            tokenAddress: NFT_CONTRACT_ADDRESS
        },
        // The minimum bid allowed for out token
        // based on the number of favorites
        startAmount: .01*parseFloat(args['favorites']), // 0.01 ETH x num favorites
        expirationTime: expirationTime,
        waitForHighestBid: true,
        paymentTokenAddress: wethAddress,
        accountAddress: OWNER_ADDRESS
    })
    // Confirm we created the auction
    console.log(`Successfully created an English auction sell order! ${englishAuctionSellOrder.asset.openseaLink}\n`)

    // exit the program
    return process.exit(0);

}

main()
