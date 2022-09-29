const { ShardingManager } = require('discord.js')
require('dotenv').config();
const Discord = require('discord.js')
const shards = new ShardingManager("./index.js", {
    token: process.env.TOKEN,
    totalShards: 2,   
    execArgv: ['--trace-warnings'],
	shardArgs: ['--ansi', '--color'],
});

shards.on('shardCreate', shard => {
    shard.on('ready', () => {
        hook.send(`\`[${new Date().toString().split(" ", 5).join(" ")}]\` <:online2:464520569975603200> Shard \`#${shard.id + 1}\`  prêt \n▬▬▬▬▬▬▬▬`)

    })
    shard.on("disconnect", (event) => {
        console.warn("Shard " + shard.id + " disconnected. Dumping socket close event...");
        console.log(event);
    });

    shard.on("disconnect", (event) => {
        console.warn("Shard " + shard.id + " disconnected. Dumping socket close event...");
         hook.send(`\`[${new Date().toString().split(" ", 5).join(" ")}]\` <:dnd2:464520569560498197> Shard \`#${shard.id + 1}\`  est déconnecté   \n▬▬▬▬▬▬▬▬ `)

        console.log(event);
    });
    shard.on("reconnecting", () => {
        console.warn("Shard " + shard.id + " is reconnecting...");
         hook.send(`\`[${new Date().toString().split(" ", 5).join(" ")}]\` <:away2:464520569862357002> Shard \`#$shard.id + 1}\` se reconnecte  \n▬▬▬▬▬▬▬▬  `)

    });
    
    console.log(`[${new Date().toString().split(" ", 5).join(" ")}] Lancé shard #${shard.id}`);
    const hook = new Discord.WebhookClient('939450778354085898', 'UgP5eF6JMcwxHDp-vMeJPC99rKbCb22ySxg1h54hvbqJmw0s8Uroy_SKSn8QpnlHsRp0');
    hook.send(`\`[${new Date().toString().split(" ", 5).join(" ")}]\` <:away2:464520569862357002> Shard \`#${shard.id + 1}\`  démarre`)
})

shards.spawn(shards.totalShards, 10000);
