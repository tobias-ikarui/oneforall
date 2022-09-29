const StateManager = require('../../utils/StateManager');
const Discord = require('discord.js');
// const { client } = require('advanced-command-handler/classes/CommandHandler');
const Event = require('../../structures/Handler/Event');
module.exports = class guildCreate extends Event {
    constructor() {
        super({
            name: 'guildCreate',
        });
    }

    async run(client, guild) {
        const newInv = await guild.fetchInvites()
        for (const [code, invite] of newInv) {
            guild.cachedInv.set(code, invite)
        }


        const { owners } = guild;
        let owner;
        if (client.botperso) {
            const fs = require('fs');
            const path = './config.json';
            if (fs.existsSync(path)) {
               owner =  await client.users.fetch(require('../../config.json').owner, true);
            } else {
                owner = await client.users.fetch(process.env.OWNER, true)
            }
        }
        if (!client.botperso) {
            owners.push(guild.ownerID);
            guild.updateOwner = owners
        }
        if (client.guilds.cache.size > 10) {
            owner.send(`Vous ne pouvez plus ajouter votre bot dans des serveurs il atteind le quota maximum de 10`)
            return guild.leave()
        }
        const guildMember = await guild.members.fetch();

        if(!guildMember.has(owner.id)){
            owner.send(`J'ai leave ${guild.name} aucune présence de l'acheteur du bot`)
            return guild.leave();
        }
        const embed = new Discord.MessageEmbed()
            .setTitle(`J'ai été ajouté a un nouveau serveur`)
            .setDescription(
                `<:778353230484471819:780727288903237663> Nom : **${guild.name}**\n
     <:778353230589460530:780725963465687060> GuildId : **${guild.id}**\n
     <:778353230383546419:781153631881265173> GuildCount : **${guild.memberCount}**\n
     <:778353230383546419:781153631881265173> OnwerName : **<@${guild.ownerID}>**\n
  `)

        await owner.send(embed);

    }
}

