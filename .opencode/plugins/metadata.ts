export const MetadataPlugin = async () => {
  const timers = new Map<string, number>()

  return {
    "tool.execute.before": async (input: any) => {
      timers.set(input.id, Date.now())
    },
    "tool.execute.after": async (input: any, output: any) => {
      const start = timers.get(input.id)
      if (!start) return
      timers.delete(input.id)
      const ms = Date.now() - start
      const time = new Date().toLocaleTimeString("en-US", { timeZone: "America/Los_Angeles", hour12: false })
      output.result += `\n[${time} PST | ${ms}ms]`
    },
  }
}
