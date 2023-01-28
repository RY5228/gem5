#include "cpu/o3/lfence_inst.hh"

#include "arch/generic/pcstate.hh"
#include "cpu/static_inst.hh"

namespace gem5
{

namespace
{

class LFence : public StaticInst
{
  public:
    LFence() : StaticInst("LFence", IntAluOp) {
        flags[IsReadBarrier] = true;
        flags[IsSerializeAfter] = true;
    }

    Fault
    execute(ExecContext *xc, trace::InstRecord *traceData) const override
    {
        return NoFault;
    }

    void
    advancePC(PCStateBase &pc) const override
    {
        pc.advance();
    }

    std::string
    generateDisassembly(Addr pc,
            const loader::SymbolTable *symtab) const override
    {
        return mnemonic;
    }
};

}

StaticInstPtr LFencePtr = new LFence;

} // namespace gem5
