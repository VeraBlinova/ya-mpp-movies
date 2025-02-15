try {
    if (rs.status().ok === 1) {
        console.log("Replica Set is already instantiated")
        exit
    }
} catch (e) {
    if (e.ok === 0) {
        rs.initiate(
            {
                _id: "mongo_cnf",
                configsvr: true,
                members: [
                    {_id: 0, host: "mongo_cnf"}
                ]
            })
        console.log("Replica Set instantiated")
    } else {
        throw e
    }
}
