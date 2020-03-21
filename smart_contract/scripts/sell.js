const opensea = require('opensea-js')
const OpenSeaPort = opensea.OpenSeaPort;
const Network = opensea.Network;
const MnemonicWalletSubprovider = require('@0x/subproviders').MnemonicWalletSubprovider
const RPCSubprovider = require('web3-provider-engine/subproviders/rpc')
const Web3ProviderEngine = require('web3-provider-engine')

const MNEMONIC = process.env.MNEMONIC
const INFURA_KEY = process.env.INFURA_KEY
const NFT_CONTRACT_ADDRESS = process.env.NFT_CONTRACT_ADDRESS
const OWNER_ADDRESS = process.env.OWNER_ADDRESS
const NETWORK = process.env.NETWORK
// const API_KEY = process.env.API_KEY || "" // API key is optional but useful if you're doing a high volume of requests.

const ArgumentParser = require('argparse').ArgumentParser;


if (!MNEMONIC || !INFURA_KEY || !NETWORK || !OWNER_ADDRESS) {
    console.error("Please set a mnemonic, infura key, owner, network, and owner adress.")
    return
}

if ( !NFT_CONTRACT_ADDRESS) {
    console.error("Please set a NFT contract address.")
    return
}

// create arg parser
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


const BASE_DERIVATION_PATH = `44'/60'/0'/0`

const mnemonicWalletSubprovider = new MnemonicWalletSubprovider({ mnemonic: MNEMONIC, baseDerivationPath: BASE_DERIVATION_PATH})
const infuraRpcSubprovider = new RPCSubprovider({
    rpcUrl: 'https://' + NETWORK + '.infura.io/v3/' + INFURA_KEY,
})

const providerEngine = new Web3ProviderEngine()
providerEngine.addProvider(mnemonicWalletSubprovider)
providerEngine.addProvider(infuraRpcSubprovider)
providerEngine.start();

const seaport = new OpenSeaPort(providerEngine, {
    networkName: NETWORK === 'mainnet' ? Network.Main : Network.Rinkeby
    //apiKey: API_KEY
}, (arg) => console.log(arg))

async function main() {

    // // // Example: Dutch auction.
    // console.log("Dutch auctioning an item...")
    // const expirationTime = Math.round(Date.now() / 1000 + 60 * 60 * 24)
    // const dutchAuctionSellOrder = await seaport.createSellOrder({
    //     tokenId: "1",
    //     tokenAddress: NFT_CONTRACT_ADDRESS,
    //     startAmount: .05,
    //     endAmount: .01,
    //     expirationTime: expirationTime,
    //     accountAddress: OWNER_ADDRESS
    // })
    // console.log(`Successfully created a dutch auction sell order! ${dutchAuctionSellOrder.asset.openseaLink}\n`)


    // English auction.
    console.log("English auctioning an item in DAI...")
    const wethAddress = NETWORK == 'mainnet' ? '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' : "0xc778417e063141139fce010982780140aa0cd5ab"
    // auction for one day ( I'll change to one week from one hour)
    const expirationTime = Math.round(Date.now() / 1000 + 60 * 60 * 24)
    const englishAuctionSellOrder = await seaport.createSellOrder({
        tokenId: String(args['id']),
        tokenAddress: NFT_CONTRACT_ADDRESS,
        startAmount: .01*parseFloat(args['favorites']), // 0.01 ETH x num favorites
        expirationTime: expirationTime,
        waitForHighestBid: true,
        paymentTokenAddress: wethAddress,
        accountAddress: OWNER_ADDRESS
    })
    console.log(`Successfully created an English auction sell order! ${englishAuctionSellOrder.asset.openseaLink}\n`)

    // exit the program
    return process.exit(0);

}

main()
