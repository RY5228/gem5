#include "cpu/o3/lsq_fence_inst.hh"

#include "arch/generic/pcstate.hh"
#include "cpu/static_inst.hh"

namespace gem5
{

namespace
{

class LSQFence : public StaticInst
{
  public:
    LSQFence() : StaticInst("LSQFence", IntAluOp) {
        flags[IsLfence] = true;
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

StaticInstPtr LSQFencePtr = new LSQFence;

} // namespace gem5
